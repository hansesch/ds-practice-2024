from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Order(_message.Message):
    __slots__ = ("orderId", "orderQuantity")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    ORDERQUANTITY_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    orderQuantity: int
    def __init__(self, orderId: _Optional[str] = ..., orderQuantity: _Optional[int] = ...) -> None: ...

class Confirmation(_message.Message):
    __slots__ = ("isSuccess", "message")
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    isSuccess: bool
    message: str
    def __init__(self, isSuccess: bool = ..., message: _Optional[str] = ...) -> None: ...
