# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: utils/pb/suggestions/suggestions.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from utils.pb.common import common_pb2 as utils_dot_pb_dot_common_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&utils/pb/suggestions/suggestions.proto\x12\x0bsuggestions\x1a\x1cutils/pb/common/common.proto\"U\n\x15InitializationRequest\x12\x0f\n\x07orderId\x18\x01 \x01(\t\x12+\n\x05items\x18\x02 \x03(\x0b\x32\x1c.suggestions.TransactionItem\"\x1f\n\x0fTransactionItem\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xc9\x01\n\x13SuggestionsResponse\x12\x11\n\tisSuccess\x18\x01 \x01(\x08\x12=\n\x05items\x18\x02 \x03(\x0b\x32..suggestions.SuggestionsResponse.SuggestedItem\x12\x14\n\x07message\x18\x03 \x01(\tH\x00\x88\x01\x01\x1a>\n\rSuggestedItem\x12\x0e\n\x06\x62ookId\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\tB\n\n\x08_message2\xa8\x01\n\x12SuggestionsService\x12K\n\x0fInitializeOrder\x12\".suggestions.InitializationRequest\x1a\x14.common.ResponseData\x12\x45\n\x0cSuggestItems\x12\x13.common.RequestData\x1a .suggestions.SuggestionsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'utils.pb.suggestions.suggestions_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_INITIALIZATIONREQUEST']._serialized_start=85
  _globals['_INITIALIZATIONREQUEST']._serialized_end=170
  _globals['_TRANSACTIONITEM']._serialized_start=172
  _globals['_TRANSACTIONITEM']._serialized_end=203
  _globals['_SUGGESTIONSRESPONSE']._serialized_start=206
  _globals['_SUGGESTIONSRESPONSE']._serialized_end=407
  _globals['_SUGGESTIONSRESPONSE_SUGGESTEDITEM']._serialized_start=333
  _globals['_SUGGESTIONSRESPONSE_SUGGESTEDITEM']._serialized_end=395
  _globals['_SUGGESTIONSSERVICE']._serialized_start=410
  _globals['_SUGGESTIONSSERVICE']._serialized_end=578
# @@protoc_insertion_point(module_scope)
