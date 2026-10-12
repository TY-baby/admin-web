from datetime import datetime, date, time
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.core.logging_conf import logger
from app.models.customer import Customer
from app.models.douyin_account import DouyinAccount
from app.models.payee import Payee
from app.models.withdraw import Withdraw
from app.schemas.common import ok, fail
from app.schemas.withdraw import WithdrawCreateReq
from app.utils.id_generator import load_items

router = APIRouter()


@router.get("/payees")
def list_payees(db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    rows = db.query(Payee).order_by(Payee.sort.asc(), Payee.id.asc()).all()
    return ok([{"id": p.id, "card_no": p.card_no, "bank_name": p.bank_name,
                "holder_name": p.holder_name, "display_name": p.display_name}
               for p in rows])


@router.get("/customers")
def list_customers_for_cascade(keyword: Optional[str] = None,
                               db: Session = Depends(get_db),
                               _a=Depends(get_current_admin)):
    q = db.query(Customer)
    if keyword:
        q = q.filter(Customer.customer_name.like(f"%{keyword}%"))
    custs = q.order_by(Customer.created_at.desc()).limit(500).all()
    cids = [c.id for c in custs]
    acc_map: dict = {}
    if cids:
        accs = (db.query(DouyinAccount)
                .filter(DouyinAccount.customer_id.in_(cids))
                .order_by(DouyinAccount.created_at.asc()).all())
        for a in accs:
            acc_map.setdefault(a.customer_id, []).append({
                "id": a.id, "douyin_id": a.douyin_id,
                "douyin_name": a.douyin_name, "nickname": a.nickname,
                "platform_code": a.platform_code,
            })
    return ok([{"id": c.id, "customer_name": c.customer_name,
                "accounts": acc_map.get(c.id, [])} for c in custs])


@router.get("/preview/{account_id}")
def preview_amount(account_id: int, db: Session = Depends(get_db),
                   _a=Depends(get_current_admin)):
    a = db.query(DouyinAccount).filter(DouyinAccount.id == account_id).first()
    if not a:
        return fail("投放ID不存在", code=40404)
    items = load_items(a.generated_items)
    payable = round(sum(float(it.get("value", 0) or 0) for it in items), 2)
    return ok({"douyin_account_id": a.id, "douyin_id": a.douyin_id,
               "douyin_name": a.douyin_name, "nickname": a.nickname,
               "generated_count": len(items), "payable_amount": payable})


@router.post("/create")
def create_withdraw(body: WithdrawCreateReq,
                    db: Session = Depends(get_db),
                    admin=Depends(get_current_admin)):
    payee = db.query(Payee).filter(Payee.id == body.payee_id).first()
    if not payee:
        return fail("打款对象不存在", code=40404)
    acc = db.query(DouyinAccount).filter(DouyinAccount.id == body.douyin_account_id).first()
    if not acc:
        return fail("投放ID不存在", code=40404)
    cust = db.query(Customer).filter(Customer.id == acc.customer_id).first()
    items = load_items(acc.generated_items)
    payable = round(sum(float(it.get("value", 0) or 0) for it in items), 2)
    operator = admin.get("username", "")
    w = Withdraw(
        payee_id=payee.id, payee_card_no=payee.card_no,
        payee_bank_name=payee.bank_name, payee_holder_name=payee.display_name,
        customer_id=cust.id if cust else 0,
        customer_name=cust.customer_name if cust else "",
        douyin_account_id=acc.id, douyin_id=acc.douyin_id,
        douyin_name=acc.douyin_name or acc.nickname,
        generated_count=len(items), payable_amount=payable,
        remark=body.remark, operator=operator,
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    logger.info(f"[withdraw created] id={w.id} payee={payee.display_name} "
                f"account={acc.douyin_id} amount={payable} operator={operator}")
    return ok({"id": w.id, "payable_amount": payable})


@router.get("/list")
def list_api(keyword: Optional[str] = None,
             date_from: Optional[date] = None, date_to: Optional[date] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    q = db.query(Withdraw)
    if keyword:
        q = q.filter(
            (Withdraw.payee_holder_name.like(f"%{keyword}%")) |
            (Withdraw.customer_name.like(f"%{keyword}%")) |
            (Withdraw.douyin_id.like(f"%{keyword}%"))
        )
    if date_from:
        q = q.filter(Withdraw.created_at >= datetime.combine(date_from, time.min))
    if date_to:
        q = q.filter(Withdraw.created_at <= datetime.combine(date_to, time.max))
    total = q.count()
    rows = (q.order_by(Withdraw.created_at.desc())
            .offset((page - 1) * page_size).limit(page_size).all())
    return ok({"total": total, "page": page, "page_size": page_size,
               "items": [{
                   "id": w.id,
                   "payee_holder_name": w.payee_holder_name,
                   "payee_bank_name": w.payee_bank_name,
                   "payee_card_no": w.payee_card_no,
                   "customer_name": w.customer_name,
                   "douyin_id": w.douyin_id,
                   "douyin_name": w.douyin_name,
                   "generated_count": w.generated_count,
                   "payable_amount": float(w.payable_amount),
                   "remark": w.remark,
                   "operator": w.operator,
                   "created_at": w.created_at.strftime("%Y-%m-%d %H:%M:%S") if w.created_at else "",
               } for w in rows]})


@router.delete("/{wid}")
def delete_withdraw(wid: int, db: Session = Depends(get_db),
                    admin=Depends(get_current_admin)):
    w = db.query(Withdraw).filter(Withdraw.id == wid).first()
    if not w:
        return fail("记录不存在", code=40404)
    db.delete(w)
    db.commit()
    logger.info(f"[withdraw deleted] id={wid} operator={admin.get('username', '')}")
    return ok()
