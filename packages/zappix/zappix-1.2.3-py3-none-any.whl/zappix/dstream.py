"""
Module containing handlers for Zabbix protocol.
"""

from ast import Return
from typing import Optional, Dict
import abc
import re
import socket
import struct
import logging
import json
import zlib
from enum import Flag, IntEnum
from OpenSSL.SSL import Context, Connection, TLSv1_2_METHOD
from openssl_psk import patch_context
from zappix.protocol import ServerInfo


logger = logging.getLogger(__name__)

# Header length. Zabbix Large Packets are not supported
ZBX_HEADER_LEN = (
    4 + # ZBXD
    1 + # Protocol flags
    4 + # Data len
    4   # Reserved or uncompressed data when using compression
)
INFO_RE = re.compile(
    r'processed: (\d+); failed: (\d+); total: (\d+); seconds spent: (\d+\.\d+)')


class ProtocolFlags(IntEnum):
    ZABBIX = 1
    COMPRESSION = 2
    LARGE_PACKET = 4


class PSKEnum(IntEnum):
    IDENTITY_MIN_LENGTH = 1
    IDENTITY_MAX_LENGTH = 128
    PSK_MIN_LENGTH = 32
    PSK_MAX_LENGTH = 512


class _Dstream(abc.ABC):
    def __init__(self, target: str, port: int = 10051, source_address: Optional[str] = None) -> None:
        self._ip = target
        self._port = port
        self._source_address = source_address
        self._timeout = None
        self._psk = b''
        self._psk_identity = b''
        self._cipherlist = b'EECDH+aRSA+AES128:RSA+aRSA+AES128:kECDHEPSK+AES128:kPSK+AES128'
        self.__compress = False

    @property
    def cipherlist(self) -> str:
        """
        Get the current cipher list.

        Returns
        -------
        :return:
            The current cipher list as string.
        """
        return self._cipherlist.decode()

    @cipherlist.setter
    def cipherlist(self, value: str) -> None:
        """
        Set the cipher list for TLS connections.

        Parameters
        ----------
        :value:
            Cipher list as a string, will be encoded to bytes.
        """
        self._cipherlist = value.encode()
        
    @property
    def compress(self) -> bool:
        """
        Get the compression setting.
        
        Returns
        -------
        :return:
            The current compression setting.
        """
        return self.__compress
        
    @compress.setter
    def compress(self, value: bool) -> None:
        """
        Enable or disable compression.
        
        Parameters
        ----------
        :value:
            True to enable compression, False to disable.
        """
        self.__compress = bool(value)

    def set_timeout(self, timeout: float):
        """
        Set timeout for the network connection

        Parameters
        ----------
        :timeout:
            Timeout in seconds.
        """
        self._timeout = timeout

    def set_psk_encryption(self, identity: str, psk: str):
        if not (PSKEnum.IDENTITY_MIN_LENGTH <= len(identity) <= PSKEnum.IDENTITY_MAX_LENGTH):
            raise ValueError("PSK identity lenght out of bounds")
        if not (PSKEnum.PSK_MIN_LENGTH <= len(psk) <= PSKEnum.PSK_MAX_LENGTH):
            raise ValueError("PSK key lenght out of bounds")

        patch_context()
        try:
            self._psk = bytes.fromhex(psk)
            self._psk_identity = identity.encode()
        except ValueError:
            raise ValueError("The provided PSK key is not hexadecimal")

    def _wrap_psk_socket(self, sock):
        def client_callback(conn, identity_hint):
            return (self._psk_identity, self._psk)
        ctx = Context(TLSv1_2_METHOD)
        ctx.set_cipher_list(self._cipherlist)
        ctx.set_psk_client_callback(client_callback)
        return Connection(ctx, sock)

    def _get_socket(self) -> socket.socket:
        address_family = socket.getaddrinfo(self._ip, self._port)[0][0]
        s = socket.socket(address_family)
        s.settimeout(self._timeout)
        return s

    def _send(self, payload: bytes) -> str:
        data = b""
        parsed = ""
        s = None
        try:
            s = self._get_socket()
            if self._source_address:
                s.bind((self._source_address, 0))
                logger.info(
                    f"Opening connection to {self._ip}:{self._port} with source address {self._source_address}")
            else:
                logger.info(f"Opening connection to {self._ip}:{self._port}")
            if self._psk and self._psk_identity:
                s = self._wrap_psk_socket(s)
            packed = self._pack_request(payload)
            s.connect((self._ip, self._port))
            s.sendall(packed)
            data = self._recv_response(s)
            parsed = self._unpack_response(data)
        except Exception as e:
            logger.exception(f"Encoutered Exception: {e}")
            raise e
        finally:
            if s is not None:
                logger.info(f"Closing connection to {self._ip}:{self._port}")
                s.close()
        return parsed

    def _unpack_response(self, response: bytes) -> str:
        """
        Unpack a response according to the Zabbix protocol.
        
        Parameters
        ----------
        :response:
            The response to unpack.
            
        Returns
        -------
        :return:
            The unpacked response as a string.
        """
        header = response[:ZBX_HEADER_LEN]
        _, flags_byte, length, reserved = struct.unpack('<4scLL', header)
        
        flags = ord(flags_byte)
        is_compressed = bool(flags & ProtocolFlags.COMPRESSION.value)
        
        # Extract the data based on the header
        data = response[ZBX_HEADER_LEN:ZBX_HEADER_LEN+length]
        
        # Decompress if necessary
        if is_compressed:
            data = zlib.decompress(data)
        
        return data.decode('utf-8')

    def _pack_request(self, payload: bytes) -> bytes:
        """
        Pack a request according to the Zabbix protocol.
        
        Parameters
        ----------
        :payload:
            The payload to pack.
            
        Returns
        -------
        :return:
            The packed request.
        """
        # Ensure payload is bytes
        if not isinstance(payload, bytes):
            raise TypeError("Payload must be a bytes object")
            
        flags = ProtocolFlags.ZABBIX
        uncompressed_len = len(payload)
        
        if self.__compress:
            compressed_data = zlib.compress(payload)
            compressed_len = len(compressed_data)
            
            flags |= ProtocolFlags.COMPRESSION
            payload = compressed_data
            payload_len = compressed_len
        else:
            # No compression
            payload_len = uncompressed_len
        
        packed = struct.pack(
            f'<4scL4s{payload_len}s',
            b'ZBXD',
            # ProtocolFlags.ZABBIX.value.to_bytes(1, 'little'),
            flags.to_bytes(1, 'little'),
            payload_len,
            uncompressed_len.to_bytes(4,"little") if (flags & ProtocolFlags.COMPRESSION) else b"\x00\x00\x00\x00",
            payload
        )
        
        logger.debug(
            f"Packed payload for {self._ip}:{self._port}. Payload length: {payload_len}. Length with headers: {len(packed)}")
        return packed

    def _recv_response(self, socket_: socket.socket, buff: int = 1024) -> bytes:
        data = b""
        buffer = socket_.recv(buff)
        _, data_length = struct.unpack('<5sQ', buffer[:ZBX_HEADER_LEN])
        logger.debug(f"Received {len(buffer)} from {self._ip}:{self._port}")
        while buffer:
            data += buffer
            if len(data[ZBX_HEADER_LEN:]) < data_length:
                buffer = socket_.recv(buff)
                logger.debug(
                    f"Received {len(buffer)} from {self._ip}:{self._port}")
            else:
                break

        logger.debug(
            f"Completed data retrieval from {self._ip}:{self._port}. Total length: {len(data)}")
        return data

    @staticmethod
    def _parse_server_response(info) -> ServerInfo:
        response = json.loads(info)
        parsed_data = INFO_RE.match(response.get('info', ''))

        server_info = ServerInfo(
            response=response.get('response'),
            processed=int(parsed_data.group(1)),
            failed=int(parsed_data.group(2)),
            total=int(parsed_data.group(3)),
            seconds_spent=float(parsed_data.group(4))
        )
        return server_info
