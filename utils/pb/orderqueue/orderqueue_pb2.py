# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: utils/pb/orderqueue/orderqueue.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$utils/pb/orderqueue/orderqueue.proto\x12\norderqueue\x1a\x1bgoogle/protobuf/empty.proto\"U\n\x05Order\x12\x0f\n\x07orderId\x18\x01 \x01(\t\x12$\n\x05items\x18\x02 \x03(\x0b\x32\x15.orderqueue.OrderItem\x12\x15\n\rorderQuantity\x18\x03 \x01(\x05\")\n\tOrderItem\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"2\n\x0c\x43onfirmation\x12\x11\n\tisSuccess\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\x85\x01\n\x11OrderQueueService\x12\x38\n\x07\x45nqueue\x12\x11.orderqueue.Order\x1a\x18.orderqueue.Confirmation\"\x00\x12\x36\n\x07\x44\x65queue\x12\x16.google.protobuf.Empty\x1a\x11.orderqueue.Order\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'utils.pb.orderqueue.orderqueue_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ORDER']._serialized_start=81
  _globals['_ORDER']._serialized_end=166
  _globals['_ORDERITEM']._serialized_start=168
  _globals['_ORDERITEM']._serialized_end=209
  _globals['_CONFIRMATION']._serialized_start=211
  _globals['_CONFIRMATION']._serialized_end=261
  _globals['_ORDERQUEUESERVICE']._serialized_start=264
  _globals['_ORDERQUEUESERVICE']._serialized_end=397
# @@protoc_insertion_point(module_scope)
