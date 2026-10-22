from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class WithdrawCreateReq(BaseModel):
    payee_id: int = Field(..., gt=0)
    douyin_account_id: Optional[int] = Field(0, ge=0)
    launch_type: str = Field(..., description="FIRST_CHARGE / EXPOSURE / NOVEL_PROMO")
    generated_count: Optional[int] = Field(0, ge=0)
    heat_value: Optional[int] = Field(0, ge=0)
    payable_amount: float = Field(..., gt=0)
    settle_date: Optional[date] = None
    remark: str = Field("", max_length=255)
    # 网文推广：客户 + 平台 + 内容（无投放ID）
    customer_id: Optional[int] = Field(None, gt=0)
    platform_code: Optional[str] = Field(None, max_length=30)
    promo_content: Optional[str] = Field(None, max_length=20)
