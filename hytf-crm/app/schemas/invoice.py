from typing import Optional
from pydantic import BaseModel, Field


class InvoiceCreateReq(BaseModel):
    customer_id: Optional[int] = None
    customer_name: str = Field("", max_length=50)
    amount: float = Field(..., gt=0)
    remark: str = Field("", max_length=255)