from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class DouyinCreateReq(BaseModel):
    douyin_id: str = Field(..., max_length=50)
    douyin_name: str = Field("", max_length=50)
    recharge_amount: float = Field(..., gt=0)
    auth_duration: str = Field("UNLIMITED")
    auth_days_custom: Optional[int] = Field(None, ge=1, le=3650)
    remark: str = Field("", max_length=255)

    @field_validator("auth_duration")
    @classmethod
    def _check(cls, v: str) -> str:
        if v not in {"UNLIMITED", "D3", "D7", "D30", "CUSTOM"}:
            raise ValueError("auth_duration illegal")
        return v


class CustomerCreateReq(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=50)
    contact_name: str = Field("", max_length=50)
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    remark: str = Field("", max_length=255)
    douyin_list: List[DouyinCreateReq] = Field(..., min_length=1)


class CustomerUpdateReq(BaseModel):
    customer_name: Optional[str] = Field(None, max_length=50)
    contact_name: Optional[str] = Field(None, max_length=50)
    remark: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class DouyinUpdateReq(BaseModel):
    douyin_name: Optional[str] = Field(None, max_length=50)
    recharge_amount: Optional[float] = Field(None, gt=0)
    auth_duration: Optional[str] = None
    auth_days_custom: Optional[int] = Field(None, ge=1, le=3650)
    status: Optional[str] = None
    remark: Optional[str] = Field(None, max_length=255)