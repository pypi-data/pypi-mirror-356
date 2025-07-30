from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FeedBoostResult(_message.Message):
    __slots__ = ["identifier_field", "response"]
    IDENTIFIER_FIELD_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    identifier_field: str
    response: str
    def __init__(self, identifier_field: _Optional[str] = ..., response: _Optional[str] = ...) -> None: ...
