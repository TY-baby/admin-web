from typing import Optional
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class ClickRequest(BaseModel):
    news_id: Optional[int] = 0
    title: str = ""
    fee: Optional[float] = 0
    url: Optional[str] = ""