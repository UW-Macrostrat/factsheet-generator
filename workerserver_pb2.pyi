from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileDataRequest(_message.Message):
    __slots__ = ["data", "title"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    data: str
    title: str
    def __init__(self, data: _Optional[str] = ..., title: _Optional[str] = ...) -> None: ...

class StratNameRequest(_message.Message):
    __slots__ = ["strat_names"]
    STRAT_NAMES_FIELD_NUMBER: _ClassVar[int]
    strat_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, strat_names: _Optional[_Iterable[str]] = ...) -> None: ...

class QueryRequest(_message.Message):
    __slots__ = ["queries"]
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    queries: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, queries: _Optional[_Iterable[str]] = ...) -> None: ...

class FactRequest(_message.Message):
    __slots__ = ["strat_name"]
    STRAT_NAME_FIELD_NUMBER: _ClassVar[int]
    strat_name: str
    def __init__(self, strat_name: _Optional[str] = ...) -> None: ...

class ErrorResponse(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: str
    def __init__(self, error: _Optional[str] = ...) -> None: ...
