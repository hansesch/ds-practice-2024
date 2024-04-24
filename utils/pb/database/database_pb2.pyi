from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

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

class PrepareResponse(_message.Message):
    __slots__ = ("isReady",)
    ISREADY_FIELD_NUMBER: _ClassVar[int]
    isReady: bool
    def __init__(self, isReady: bool = ...) -> None: ...

class CommitRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CommitResponse(_message.Message):
    __slots__ = ("isSuccess",)
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    isSuccess: bool
    def __init__(self, isSuccess: bool = ...) -> None: ...

class PrepareWriteRequest(_message.Message):
    __slots__ = ("id", "stockValue")
    ID_FIELD_NUMBER: _ClassVar[int]
    STOCKVALUE_FIELD_NUMBER: _ClassVar[int]
    id: str
    stockValue: int
    def __init__(self, id: _Optional[str] = ..., stockValue: _Optional[int] = ...) -> None: ...

class PrepareDecrementStockRequest(_message.Message):
    __slots__ = ("id", "decrement")
    ID_FIELD_NUMBER: _ClassVar[int]
    DECREMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    decrement: int
    def __init__(self, id: _Optional[str] = ..., decrement: _Optional[int] = ...) -> None: ...
