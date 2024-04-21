from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Order(_message.Message):
    __slots__ = ("orderId", "items", "orderQuantity")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    ORDERQUANTITY_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    items: _containers.RepeatedCompositeFieldContainer[OrderItem]
    orderQuantity: int
    def __init__(self, orderId: _Optional[str] = ..., items: _Optional[_Iterable[_Union[OrderItem, _Mapping]]] = ..., orderQuantity: _Optional[int] = ...) -> None: ...

class OrderItem(_message.Message):
    __slots__ = ("id", "quantity")
    ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    quantity: int
    def __init__(self, id: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class Confirmation(_message.Message):
    __slots__ = ("isSuccess", "message")
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    isSuccess: bool
    message: str
    def __init__(self, isSuccess: bool = ..., message: _Optional[str] = ...) -> None: ...
