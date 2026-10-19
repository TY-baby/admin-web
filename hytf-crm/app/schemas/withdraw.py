from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class WithdrawCreateReq(BaseModel):
    payee_id: int = Field(..., gt=0)
    douyin_account_id: int = Field(..., gt=0)
    launch_type: str = Field(..., description="FIRST_CHARGE / EXPOSURE")
    generated_count: Optional[int] = Field(0, ge=0)
    heat_value: Optional[int] = Field(0, ge=0)
    payable_amount: float = Field(..., gt=0)
    settle_date: Optional[date] = None
    remark: str = Field("", max_length=255)