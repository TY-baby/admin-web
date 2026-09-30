from datetime import date
from pydantic import BaseModel, Field


class WithdrawCreateReq(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    pay_date: date
    id_count: int = Field(..., ge=0)
    payable_amount: float = Field(..., ge=0)
    remark: str = Field("", max_length=255)