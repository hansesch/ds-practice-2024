from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReadRequest(_message.Message):
    __slots__ = ("title",)
    TITLE_FIELD_NUMBER: _ClassVar[int]
    title: str
    def __init__(self, title: _Optional[str] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ("stockValue",)
    STOCKVALUE_FIELD_NUMBER: _ClassVar[int]
    stockValue: int
    def __init__(self, stockValue: _Optional[int] = ...) -> None: ...

class WriteRequest(_message.Message):
    __slots__ = ("title", "stockValue")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    STOCKVALUE_FIELD_NUMBER: _ClassVar[int]
    title: str
    stockValue: int
    def __init__(self, title: _Optional[str] = ..., stockValue: _Optional[int] = ...) -> None: ...

class WriteResponse(_message.Message):
    __slots__ = ("stockValue",)
    STOCKVALUE_FIELD_NUMBER: _ClassVar[int]
    stockValue: int
    def __init__(self, stockValue: _Optional[int] = ...) -> None: ...
