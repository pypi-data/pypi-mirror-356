from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FeedBoostStatistic(_message.Message):
    __slots__ = ["cached_tokens", "completion_tokens", "execution_time", "optimized_products", "prompt_tokens", "task_id", "timestamp", "total_input_products"]
    CACHED_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_TIME_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZED_PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TOTAL_INPUT_PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    cached_tokens: int
    completion_tokens: int
    execution_time: float
    optimized_products: int
    prompt_tokens: int
    task_id: str
    timestamp: str
    total_input_products: int
    def __init__(self, task_id: _Optional[str] = ..., timestamp: _Optional[str] = ..., cached_tokens: _Optional[int] = ..., prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., execution_time: _Optional[float] = ..., optimized_products: _Optional[int] = ..., total_input_products: _Optional[int] = ...) -> None: ...
