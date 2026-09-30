from datetime import datetime, date, time
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.models.withdraw import Withdraw
from app.schemas.common import ok, fail
from app.schemas.withdraw import WithdrawCreateReq

router = APIRouter()


@router.get("/list")
def list_api(keyword_name: Optional[str] = None,
             date_from: Optional[date] = None, date_to: Optional[date] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    q = db.query(Withdraw)
    if keyword_name:
        q = q.filter(Withdraw.name.like(f"%{keyword_name}%"))
    if date_from:
        q = q.filter(Withdraw.pay_date >= date_from)
    if date_to:
        q = q.filter(Withdraw.pay_date <= date_to)
    total = q.count()
    items = q.order_by(Withdraw.pay_date.desc(), Withdraw.id.desc()) \
        .offset((page - 1) * page_size).limit(page_size).all()
    return ok({"total": total, "page": page, "page_size": page_size,
               "items": [{"id": w.id, "name": w.name,
                          "pay_date": w.pay_date.isoformat() if w.pay_date else "",
                          "id_count": w.id_count, "payable_amount": float(w.payable_amount),
                          "remark": w.remark, "created_at": w.created_at} for w in items]})


@router.post("/create")
def create_api(body: WithdrawCreateReq,
               db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    w = Withdraw(name=body.name, pay_date=body.pay_date, id_count=body.id_count,
                 payable_amount=body.payable_amount, remark=body.remark)
    db.add(w)
    db.commit()
    db.refresh(w)
    return ok({"id": w.id})


@router.delete("/{wid}")
def delete_api(wid: int, db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    w = db.query(Withdraw).filter(Withdraw.id == wid).first()
    if not w:
        return fail("记录不存在", code=40404)
    db.delete(w)
    db.commit()
    return ok()