from common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InitializationRequest(_message.Message):
    __slots__ = ("orderId", "items")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    items: _containers.RepeatedCompositeFieldContainer[TransactionItem]
    def __init__(self, orderId: _Optional[str] = ..., items: _Optional[_Iterable[_Union[TransactionItem, _Mapping]]] = ...) -> None: ...

class TransactionItem(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class SuggestionsResponse(_message.Message):
    __slots__ = ("isSuccess", "items", "message")
    class SuggestedItem(_message.Message):
        __slots__ = ("bookId", "title", "author")
        BOOKID_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        AUTHOR_FIELD_NUMBER: _ClassVar[int]
        bookId: str
        title: str
        author: str
        def __init__(self, bookId: _Optional[str] = ..., title: _Optional[str] = ..., author: _Optional[str] = ...) -> None: ...
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    isSuccess: bool
    items: _containers.RepeatedCompositeFieldContainer[SuggestionsResponse.SuggestedItem]
    message: str
    def __init__(self, isSuccess: bool = ..., items: _Optional[_Iterable[_Union[SuggestionsResponse.SuggestedItem, _Mapping]]] = ..., message: _Optional[str] = ...) -> None: ...
