from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChatRequest(_message.Message):
    __slots__ = ["system_text", "user_text"]
    SYSTEM_TEXT_FIELD_NUMBER: _ClassVar[int]
    USER_TEXT_FIELD_NUMBER: _ClassVar[int]
    system_text: str
    user_text: str
    def __init__(self, system_text: _Optional[str] = ..., user_text: _Optional[str] = ...) -> None: ...

class ChatResponse(_message.Message):
    __slots__ = ["text"]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...
