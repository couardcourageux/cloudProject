# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protocol.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eprotocol.proto\x12\x07KVStore\"\t\n\x07VoidMsg\"\x1f\n\tSimpleMsg\x12\x12\n\nrespStatus\x18\x01 \x01(\x03\"2\n\nPayloadMsg\x12\x12\n\nrespStatus\x18\x01 \x01(\x03\x12\x10\n\x08jsonData\x18\x02 \x01(\t2\xa4\x01\n\x07KvStore\x12,\n\x04ping\x12\x10.KVStore.VoidMsg\x1a\x10.KVStore.VoidMsg\"\x00\x12\x33\n\x08obtainId\x12\x10.KVStore.VoidMsg\x1a\x13.KVStore.PayloadMsg\"\x00\x12\x36\n\x08\x66indNode\x12\x13.KVStore.PayloadMsg\x1a\x13.KVStore.PayloadMsg\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protocol_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _VOIDMSG._serialized_start=27
  _VOIDMSG._serialized_end=36
  _SIMPLEMSG._serialized_start=38
  _SIMPLEMSG._serialized_end=69
  _PAYLOADMSG._serialized_start=71
  _PAYLOADMSG._serialized_end=121
  _KVSTORE._serialized_start=124
  _KVSTORE._serialized_end=288
# @@protoc_insertion_point(module_scope)
