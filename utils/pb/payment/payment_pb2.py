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


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1eutils/pb/payment/payment.proto\x12\x07payment\x1a\x1bgoogle/protobuf/empty.proto\"!\n\x0ePrepareRequest\x12\x0f\n\x07orderId\x18\x01 \x01(\t\"\"\n\x0fPrepareResponse\x12\x0f\n\x07isReady\x18\x01 \x01(\x08\" \n\rCommitRequest\x12\x0f\n\x07orderId\x18\x01 \x01(\t\"#\n\x0e\x43ommitResponse\x12\x11\n\tisSuccess\x18\x01 \x01(\x08\x32\x96\x01\n\x0ePaymentService\x12\x43\n\x0ePreparePayment\x12\x17.payment.PrepareRequest\x1a\x18.payment.PrepareResponse\x12?\n\rCommitPayment\x12\x16.payment.CommitRequest\x1a\x16.google.protobuf.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'utils.pb.payment.payment_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PREPAREREQUEST']._serialized_start=72
  _globals['_PREPAREREQUEST']._serialized_end=105
  _globals['_PREPARERESPONSE']._serialized_start=107
  _globals['_PREPARERESPONSE']._serialized_end=141
  _globals['_COMMITREQUEST']._serialized_start=143
  _globals['_COMMITREQUEST']._serialized_end=175
  _globals['_COMMITRESPONSE']._serialized_start=177
  _globals['_COMMITRESPONSE']._serialized_end=212
  _globals['_PAYMENTSERVICE']._serialized_start=215
  _globals['_PAYMENTSERVICE']._serialized_end=365
# @@protoc_insertion_point(module_scope)
