"""
Module containing models for Zabbix protocol.
"""

from typing import List, Any, Optional, Dict, Union
from dataclasses import dataclass
import abc
import json
from ast import literal_eval
from uuid import uuid4


class _Model(abc.ABC):
    __slots__: List[str] = []

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return str(ModelEncoder().default(self))

    def to_bytes(self):
        return json.dumps(self, cls=ModelEncoder).encode("utf-8")


class ModelEncoder(json.JSONEncoder):
    """
    Class for encoding to JSON models implemented herein.
    """

    def default(self, o: _Model) -> Dict[str, Any]:
        d = {}
        for k in type(o).__slots__:
            v = getattr(o, k, None)
            if v is None:
                continue
            else:
                d[k] = v
        return d


class ItemData(_Model):
    """
    Class model representing data to be sent to a trapper item.

    Parameters
    ----------
    :host:
        Hostname to which the item belongs.
    :key:
        Item key
    :value:
        Value to be sent.
    :clock:
        Timestamp at which value was collected.
    :ns:
        Nanoseconds for clock.
    """
    __slots__ = ['host', 'key', 'value', 'clock', 'ns']

    def __init__(self, host: str, key: str, value: Any, clock: Optional[int] = None, ns: Optional[int] = None) -> None:
        super().__init__()
        self.host = host
        self.key = key
        self.value = value
        self.clock = clock
        self.ns = ns


SenderData = ItemData


class AgentData(ItemData):
    """
    Class model representing data to be sent to a Zabbix agent (active) item.

    Parameters
    ----------
    :host:
        Hostname to which the item belongs.
    :key:
        Item key
    :value:
        Value to be sent.
    :clock:
        Timestamp at which value was collected.
    :ns:
        Nanoseconds for clock
    :state:
        State of an item. Set to 1 for Unsupported.

    Attributes
    ----------
    :id:
        Unique id for item within one session.
    """
    __slots__ = ['host', 'key', 'value', 'clock', 'ns', 'id', 'state']

    def __init__(self, host: str, key: str, value: Any, clock: int, ns: int, state: Optional[int] = None) -> None:
        super().__init__(host, key, value, clock)
        self.ns = ns
        self.id = None
        self.state = state


class _TrapperRequest(_Model, abc.ABC):
    __slots__ = ['request', 'data', 'host', 'clock', 'ns', 'session']
    __supported_requests = ["active checks", "agent data",
                            "sender data", "queue.get", "status.get", "item.test", "preprocessing.test"]

    def __init__(self, request: str, **kwargs) -> None:
        super().__init__()
        if request not in _TrapperRequest.__supported_requests:
            raise ValueError("Unsupported request: %s" % request)
        self.request = request
        self.host = kwargs.get('host')
        tmp_data = kwargs.get('data')
        if request not in ["item.test", "preprocessing.test"] and tmp_data:
            self._check_items_classes(tmp_data, kwargs.get('item_class'))
            self.data = tmp_data
        elif request in ["queue.get", "status.get"]:
            self.data = None
        else:
            self.data = tmp_data if tmp_data else []
        self.clock = kwargs.get('clock')
        self.ns = kwargs.get('ns')
        self.session = kwargs.get('session')

    def _check_items_classes(self, items, item_class):
        if not all(self._check_item_class(i, item_class) for i in items):
            raise TypeError

    def _check_item_class(self, item, item_class):
        return isinstance(item, item_class)


class ActiveChecksRequest(_TrapperRequest):
    """
    Class implementing protocol for requesting active checks for host.

    Parameters
    ----------
    :host:
        Get active checks for specified host.
    """

    def __init__(self, host: str) -> None:
        super().__init__(request="active checks", host=host)
        self.data = None


class SenderDataRequest(_TrapperRequest):
    """
    Class implementing protocol for sending data with sender protocol.

    Parameters
    ----------
    :data:
        List of SenderData objects.
    """
    __item_class = SenderData

    def __init__(self, data: Optional[List[SenderData]] = None) -> None:
        super().__init__(
            request="sender data",
            data=data,
            item_class=SenderDataRequest.__item_class
        )

    def add_item(self, item: SenderData) -> None:
        """
        Add data to request.

        Parameters
        ----------
        :item:
            Instance of SenderData.
        """
        if not self._check_item_class(item, SenderDataRequest.__item_class):
            raise TypeError
        self.data.append(item)


class AgentDataRequest(_TrapperRequest):
    """
    Class implementing protocol for sending data gathered by active checks.
    Each instance should be used as unique data session.

    Parameters
    ----------
    :data:
        List of AgentData objects.
    """
    __item_class = AgentData

    def __init__(self, data: Optional[List[AgentData]] = None) -> None:
        super().__init__(
            request="agent data",
            data=data,
            item_class=AgentDataRequest.__item_class,
            session=uuid4().hex
        )

        self._item_id = 1
        if self.data:
            for d in self.data:
                d.id = self._item_id
                self._item_id += 1

    def add_item(self, item: AgentData) -> None:
        """
        Add data to request and assign an id to it.

        Parameters
        ----------
        :item:
            Instance of AgentData.
        """
        if not self._check_item_class(item, AgentDataRequest.__item_class):
            raise TypeError
        item.id = self._item_id
        self.data.append(item)
        self._item_id += 1


class ActiveItem:
    """
    Zabbix active item configuration.
    """

    __slots__ = ['key', 'delay', 'lastlogsize', 'mtime']

    def __init__(self, key: str, delay: str, lastlogsize: int = 0, mtime: int = 0) -> None:
        self.key = key
        self.delay = delay
        self.lastlogsize = lastlogsize
        self.mtime = mtime


class ServerRequest(_TrapperRequest):

    __slots__ = ['request', 'type', 'sid', 'limit', 'data']
    __supported_request_types = ['overview',
                                 'overview by proxy', 'details', 'ping', 'item.test', 'preprocessing.test']

    def __init__(self, request, request_type, sid, **kwargs) -> None:
        if request_type not in ServerRequest.__supported_request_types:
            raise ValueError("Unsupported request_type: %s" % request_type)
        if 'item_data' in kwargs:
            super().__init__(request=request, type=request_type, sid=sid, data=kwargs["item_data"])
        else:
            super().__init__(request=request, type=request_type, sid=sid)
        self.request = request
        self.type = request_type if request_type != "item.test" else None
        self.sid = sid
        if 'limit' in kwargs:
            self.limit = str(kwargs.get("limit"))


@dataclass
class ServerInfo:
    """
    Info on items processed by the server.
    """
    processed: int
    failed: int
    total: int
    seconds_spent: float
    response: str
