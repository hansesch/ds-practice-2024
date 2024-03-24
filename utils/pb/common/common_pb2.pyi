from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RequestData(_message.Message):
    __slots__ = ("orderId", "vectorClock")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    VECTORCLOCK_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    vectorClock: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, orderId: _Optional[str] = ..., vectorClock: _Optional[_Iterable[int]] = ...) -> None: ...

class ResponseData(_message.Message):
    __slots__ = ("isSuccess", "message")
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    isSuccess: bool
    message: str
    def __init__(self, isSuccess: bool = ..., message: _Optional[str] = ...) -> None: ...
