# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: utils/pb/payment/payment.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1eutils/pb/payment/payment.proto\x12\x07payment\"!\n\x0ePrepareRequest\x12\x0f\n\x07orderId\x18\x01 \x01(\t\"\"\n\x0fPrepareResponse\x12\x0f\n\x07isReady\x18\x01 \x01(\x08\" \n\rCommitRequest\x12\x0f\n\x07orderId\x18\x01 \x01(\t\"#\n\x0e\x43ommitResponse\x12\x11\n\tisSuccess\x18\x01 \x01(\x08\x32\x97\x01\n\x0ePaymentService\x12\x43\n\x0ePreparePayment\x12\x17.payment.PrepareRequest\x1a\x18.payment.PrepareResponse\x12@\n\rCommitPayment\x12\x16.payment.CommitRequest\x1a\x17.payment.CommitResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'utils.pb.payment.payment_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PREPAREREQUEST']._serialized_start=43
  _globals['_PREPAREREQUEST']._serialized_end=76
  _globals['_PREPARERESPONSE']._serialized_start=78
  _globals['_PREPARERESPONSE']._serialized_end=112
  _globals['_COMMITREQUEST']._serialized_start=114
  _globals['_COMMITREQUEST']._serialized_end=146
  _globals['_COMMITRESPONSE']._serialized_start=148
  _globals['_COMMITRESPONSE']._serialized_end=183
  _globals['_PAYMENTSERVICE']._serialized_start=186
  _globals['_PAYMENTSERVICE']._serialized_end=337
# @@protoc_insertion_point(module_scope)
