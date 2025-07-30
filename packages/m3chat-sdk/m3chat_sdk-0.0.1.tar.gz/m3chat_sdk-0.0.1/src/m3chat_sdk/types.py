from typing import TypedDict, Optional

class RequestParams(TypedDict):
    model: str
    content: str

class ClientOptions(TypedDict, total=False):
    stream: bool

class BatchOptions(TypedDict, total=False):
    model: Optional[str]
