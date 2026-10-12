from typing import Optional
from pydantic import BaseModel, Field


class WithdrawCreateReq(BaseModel):
    payee_id: int = Field(..., gt=0)
    douyin_account_id: int = Field(..., gt=0)
    remark: str = Field("", max_length=255)