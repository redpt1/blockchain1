# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: p2pseed.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rp2pseed.proto\"(\n\x15\x46indOnlineNodeRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"&\n\x16\x46indOnlineNodeResponse\x12\x0c\n\x04port\x18\x01 \x03(\x05\"-\n\x0cHelloRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\".\n\rHelloResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x03(\x05\x32x\n\x07P2pSeed\x12(\n\x05Hello\x12\r.HelloRequest\x1a\x0e.HelloResponse\"\x00\x12\x43\n\x0e\x46indOnlineNode\x12\x16.FindOnlineNodeRequest\x1a\x17.FindOnlineNodeResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'p2pseed_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _FINDONLINENODEREQUEST._serialized_start=17
  _FINDONLINENODEREQUEST._serialized_end=57
  _FINDONLINENODERESPONSE._serialized_start=59
  _FINDONLINENODERESPONSE._serialized_end=97
  _HELLOREQUEST._serialized_start=99
  _HELLOREQUEST._serialized_end=144
  _HELLORESPONSE._serialized_start=146
  _HELLORESPONSE._serialized_end=192
  _P2PSEED._serialized_start=194
  _P2PSEED._serialized_end=314
# @@protoc_insertion_point(module_scope)
