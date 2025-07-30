import unittest
from zappix.dstream import _Dstream, ProtocolFlags
import zlib


class TestDstream(unittest.TestCase):
    def test_response_after_sending_collected_data(self):
        response = _Dstream._parse_server_response(
            '{"response":"success", "info":"processed: 3; failed: 0; total: 3; seconds spent: 0.003534"}'
        )
        self.assertEqual(response.response, "success")
        self.assertEqual(response.processed, 3)
        self.assertEqual(response.failed, 0)
        self.assertEqual(response.total, 3)
        self.assertAlmostEqual(response.seconds_spent, 0.003534)

    def test_compression_setting(self):
        """Test that compression can be enabled and disabled."""
        # Create a concrete implementation of the abstract class for testing
        class ConcreteDstream(_Dstream):
            def __init__(self):
                super().__init__("localhost", 10051)

            # Expose protected methods for testing
            def pack_request(self, payload):
                return self._pack_request(payload)

        ds = ConcreteDstream()
        ds.compress = True
        self.assertTrue(ds.compress, "Compression should be enabled after setting to True")

        ds.compress = False
        self.assertFalse(ds.compress, "Compression should be disabled after setting to False")


    def test_pack_request_with_compression(self):
        """Test that _pack_request uses compression when enabled."""
        # Create a concrete implementation of the abstract class for testing
        class ConcreteDstream(_Dstream):
            def __init__(self):
                super().__init__("localhost", 10051)

            # Expose protected methods for testing
            def pack_request(self, payload):
                return self._pack_request(payload)

        ds = ConcreteDstream()
        ds.compress = True

        # Create compressible payload (repeating data compresses well)
        payload = b"a" * 1000

        # Test with compression enabled (default)
        packed_compressed = ds.pack_request(payload)

        # Check for compression flag in the header
        protocol, flags_byte, _, _ = packed_compressed[0:4], packed_compressed[4:5], packed_compressed[5:9], packed_compressed[9:13]
        flags = ord(flags_byte)
        self.assertEqual(protocol, b'ZBXD', "Protocol header should be ZBXD")
        self.assertTrue(flags & ProtocolFlags.COMPRESSION.value, "Compression flag should be set")

        # Test with compression disabled
        ds.compress = False
        packed_uncompressed = ds.pack_request(payload)

        # Check compression flag is not set
        protocol, flags_byte, _, _ = packed_uncompressed[0:4], packed_uncompressed[4:5], packed_uncompressed[5:9], packed_uncompressed[9:13]
        flags = ord(flags_byte)
        self.assertEqual(protocol, b'ZBXD', "Protocol header should be ZBXD")
        self.assertFalse(flags & ProtocolFlags.COMPRESSION.value, "Compression flag should not be set")

        # Verify compressed data is smaller than uncompressed
        self.assertLess(len(packed_compressed), len(packed_uncompressed),
                      "Compressed data should be smaller than uncompressed data")

if __name__ == '__main__':
    unittest.main()
