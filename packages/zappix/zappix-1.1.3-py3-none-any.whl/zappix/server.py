"""
Implementation of Zabbix server communication.
"""

from zappix.dstream import _Dstream
from zappix.protocol import ServerRequest
from enum import Enum
import json
from typing import Dict


class ServerRequestTypeEnum(Enum):
    OVERVIEW = "overview"
    OVERVIEW_BY_PROXY = "overwiew by proxy"
    DETAILS = "details"


QueueType = ServerRequestTypeEnum


class Server(_Dstream):
    """
    Class used for direct communication with Zabbix Server.
    Used for retrieving item queue, server health and more.

    Parameters
    ----------
    :address:
        Server address.
    :sid:
        Session id user for authorization.
    :port:
        Port the server listens on.
    """

    def __init__(self, address: str, sid: str, port: int = 10051):
        super().__init__(address, port=port)
        self._sid = sid

    def get_queue(self, queue_type: QueueType, **kwargs) -> Dict:
        """
        Get list of items waiting in monitoring queue.

        Parameters
        ----------
        :queue_type:
            Queue to check.
        :**kwargs:
            Additional parameters passed to the ServerRequest.

        Returns
        -------
        dict
            A detailed information on the queue,
        """
        if queue_type == QueueType.DETAILS and 'limit' not in kwargs:
            kwargs['limit'] = "100"
        payload = ServerRequest(
            'queue.get', queue_type.value, self._sid, **kwargs)
        response = self._send(payload.to_bytes())
        return json.loads(response)

    def test_item(self, test_type, item_data: Dict) -> Dict:
        """
        Test preprocessing

        Parameters
        ----------
        :test_type:
            Type of test. item.test or preprocessing.test
        :item_data:
            Preprocessing configuraton

        Returns
        -------
        dict
        
        """
        payload = ServerRequest(
            test_type, "item.test", self._sid, item_data=item_data
        )
        payload.type = None # remove pointles field
        response = self._send(payload.to_bytes())
        return json.loads(response)

    @property
    def is_alive(self) -> bool:
        """
        Check if the server is alive.
        This is the check the GUI performs to determine server health.

        Returns
        -------
        bool
            Whether the server is responding.
        """
        payload = ServerRequest('status.get', "ping", self._sid)
        response = self._send(payload.to_bytes())
        if json.loads(response) == {"response": "success", "data": {}}:
            return True
        return False
