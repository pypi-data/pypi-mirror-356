from fastapi.responses import JSONResponse
from typing import TypedDict, Any

class Result(TypedDict):
    ok: bool
    message: str | None
    result: Any

class Json(JSONResponse):

    def __init__(
            self, 
            content: Result,
            status_code = 200, 
            headers = None, 
            media_type = None, 
            background = None
        ):
        super().__init__(content, status_code, headers, media_type, background)