# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: suggestions.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11suggestions.proto\x12\x0bsuggestions\"#\n\x12SuggestionsRequest\x12\r\n\x05items\x18\x01 \x03(\t\"\x94\x01\n\x13SuggestionsResponse\x12=\n\x05items\x18\x01 \x03(\x0b\x32..suggestions.SuggestionsResponse.SuggestedItem\x1a>\n\rSuggestedItem\x12\x0e\n\x06\x62ookId\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t2g\n\x12SuggestionsService\x12Q\n\x0cSuggestItems\x12\x1f.suggestions.SuggestionsRequest\x1a .suggestions.SuggestionsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'suggestions_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SUGGESTIONSREQUEST']._serialized_start=34
  _globals['_SUGGESTIONSREQUEST']._serialized_end=69
  _globals['_SUGGESTIONSRESPONSE']._serialized_start=72
  _globals['_SUGGESTIONSRESPONSE']._serialized_end=220
  _globals['_SUGGESTIONSRESPONSE_SUGGESTEDITEM']._serialized_start=158
  _globals['_SUGGESTIONSRESPONSE_SUGGESTEDITEM']._serialized_end=220
  _globals['_SUGGESTIONSSERVICE']._serialized_start=222
  _globals['_SUGGESTIONSSERVICE']._serialized_end=325
# @@protoc_insertion_point(module_scope)
