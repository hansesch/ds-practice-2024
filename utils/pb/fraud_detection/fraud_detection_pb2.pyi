from common import common_pb2 as _common_pb2
from suggestions import suggestions_pb2 as _suggestions_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class InitializationRequest(_message.Message):
    __slots__ = ("orderId", "creditCardNumber", "creditCardExpirationDate", "creditCardCVV", "discountCode")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    CREDITCARDNUMBER_FIELD_NUMBER: _ClassVar[int]
    CREDITCARDEXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    CREDITCARDCVV_FIELD_NUMBER: _ClassVar[int]
    DISCOUNTCODE_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    creditCardNumber: str
    creditCardExpirationDate: str
    creditCardCVV: str
    discountCode: str
    def __init__(self, orderId: _Optional[str] = ..., creditCardNumber: _Optional[str] = ..., creditCardExpirationDate: _Optional[str] = ..., creditCardCVV: _Optional[str] = ..., discountCode: _Optional[str] = ...) -> None: ...
