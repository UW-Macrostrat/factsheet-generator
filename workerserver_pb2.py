# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: workerserver.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12workerserver.proto\".\n\x0f\x46ileDataRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\"\'\n\x10StratNameRequest\x12\x13\n\x0bstrat_names\x18\x01 \x03(\t\"\x1f\n\x0cQueryRequest\x12\x0f\n\x07queries\x18\x01 \x03(\t\"!\n\x0b\x46\x61\x63tRequest\x12\x12\n\nstrat_name\x18\x01 \x01(\t\"\x1e\n\rErrorResponse\x12\r\n\x05\x65rror\x18\x01 \x01(\t2\xd5\x01\n\x0cWorkerServer\x12/\n\tStoreFile\x12\x10.FileDataRequest\x1a\x0e.ErrorResponse\"\x00\x12\x34\n\rSetStratNames\x12\x11.StratNameRequest\x1a\x0e.ErrorResponse\"\x00\x12-\n\nSetQueries\x12\r.QueryRequest\x1a\x0e.ErrorResponse\"\x00\x12/\n\rGenerateFacts\x12\x0c.FactRequest\x1a\x0e.ErrorResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'workerserver_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FILEDATAREQUEST']._serialized_start=22
  _globals['_FILEDATAREQUEST']._serialized_end=68
  _globals['_STRATNAMEREQUEST']._serialized_start=70
  _globals['_STRATNAMEREQUEST']._serialized_end=109
  _globals['_QUERYREQUEST']._serialized_start=111
  _globals['_QUERYREQUEST']._serialized_end=142
  _globals['_FACTREQUEST']._serialized_start=144
  _globals['_FACTREQUEST']._serialized_end=177
  _globals['_ERRORRESPONSE']._serialized_start=179
  _globals['_ERRORRESPONSE']._serialized_end=209
  _globals['_WORKERSERVER']._serialized_start=212
  _globals['_WORKERSERVER']._serialized_end=425
# @@protoc_insertion_point(module_scope)
