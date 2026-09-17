from typing import Any, Optional
from pydantic import BaseModel


class Resp(BaseModel):
    code: int = 0
    msg: str = "ok"
    data: Optional[Any] = None


def ok(data=None, msg: str = "ok") -> dict:
    return {"code": 0, "msg": msg, "data": data}


def fail(msg: str = "error", code: int = 1, data=None) -> dict:
    return {"code": code, "msg": msg, "data": data}