from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReadRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ("stockValue",)
    STOCKVALUE_FIELD_NUMBER: _ClassVar[int]
    stockValue: int
    def __init__(self, stockValue: _Optional[int] = ...) -> None: ...

class WriteRequest(_message.Message):
    __slots__ = ("id", "stockValue", "hosts", "ports")
    ID_FIELD_NUMBER: _ClassVar[int]
    STOCKVALUE_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    stockValue: int
    hosts: _containers.RepeatedScalarFieldContainer[str]
    ports: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., stockValue: _Optional[int] = ..., hosts: _Optional[_Iterable[str]] = ..., ports: _Optional[_Iterable[str]] = ...) -> None: ...

class WriteResponse(_message.Message):
    __slots__ = ("isSuccess", "failedhost", "failedport")
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILEDHOST_FIELD_NUMBER: _ClassVar[int]
    FAILEDPORT_FIELD_NUMBER: _ClassVar[int]
    isSuccess: bool
    failedhost: str
    failedport: str
    def __init__(self, isSuccess: bool = ..., failedhost: _Optional[str] = ..., failedport: _Optional[str] = ...) -> None: ...
