from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InitializationRequest(_message.Message):
    __slots__ = ("orderId", "items", "userName", "userContact", "discountCode", "billingAddress", "creditCard")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    USERCONTACT_FIELD_NUMBER: _ClassVar[int]
    DISCOUNTCODE_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    items: _containers.RepeatedCompositeFieldContainer[TransactionItem]
    userName: str
    userContact: str
    discountCode: str
    billingAddress: BillingAddressInfo
    creditCard: CreditCardInfo
    def __init__(self, orderId: _Optional[str] = ..., items: _Optional[_Iterable[_Union[TransactionItem, _Mapping]]] = ..., userName: _Optional[str] = ..., userContact: _Optional[str] = ..., discountCode: _Optional[str] = ..., billingAddress: _Optional[_Union[BillingAddressInfo, _Mapping]] = ..., creditCard: _Optional[_Union[CreditCardInfo, _Mapping]] = ...) -> None: ...

class RequestData(_message.Message):
    __slots__ = ("orderId", "vectorClock")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    VECTORCLOCK_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    vectorClock: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, orderId: _Optional[str] = ..., vectorClock: _Optional[_Iterable[int]] = ...) -> None: ...

class ResponseData(_message.Message):
    __slots__ = ("isSuccess",)
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    isSuccess: bool
    def __init__(self, isSuccess: bool = ...) -> None: ...

class TransactionItem(_message.Message):
    __slots__ = ("name", "quantity")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    quantity: int
    def __init__(self, name: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class BillingAddressInfo(_message.Message):
    __slots__ = ("street", "city", "state", "zip", "country")
    STREET_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ZIP_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    street: str
    city: str
    state: str
    zip: str
    country: str
    def __init__(self, street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zip: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class CreditCardInfo(_message.Message):
    __slots__ = ("number", "expirationDate", "cvv")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    number: str
    expirationDate: str
    cvv: str
    def __init__(self, number: _Optional[str] = ..., expirationDate: _Optional[str] = ..., cvv: _Optional[str] = ...) -> None: ...
