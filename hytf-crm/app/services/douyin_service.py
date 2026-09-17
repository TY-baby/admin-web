from datetime import datetime, date, timedelta
from typing import List
from sqlalchemy import func, and_, case
from sqlalchemy.orm import Session
from app.models.douyin_account import DouyinAccount
from app.models.finance_log import FinanceLog


def get_home_summary(db: Session, cid: int) -> dict:
    accs = db.query(DouyinAccount).filter(DouyinAccount.customer_id == cid).all()
    total_balance = sum(float(a.balance) for a in accs)
    total_recharge = sum(float(a.recharge_amount) for a in accs)
    consume = db.query(func.coalesce(func.sum(-FinanceLog.amount), 0)).filter(
        and_(FinanceLog.customer_id == cid, FinanceLog.change_type == "CONSUME")).scalar() or 0
    return {"total_balance": float(total_balance), "total_recharge": float(total_recharge),
            "total_consume": float(consume), "account_count": len(accs)}


def get_trend(db: Session, cid: int, aid, dfrom: date, dto: date) -> List[dict]:
    start_dt = datetime.combine(dfrom, datetime.min.time())
    end_dt = datetime.combine(dto, datetime.max.time())
    consume_expr = func.coalesce(func.sum(case((FinanceLog.change_type == "CONSUME", -FinanceLog.amount), else_=0)), 0)
    recharge_expr = func.coalesce(func.sum(case((FinanceLog.change_type == "RECHARGE", FinanceLog.amount), else_=0)), 0)
    q = db.query(func.date(FinanceLog.stat_date).label("d"),
                 consume_expr.label("consume"),
                 recharge_expr.label("recharge")).filter(
        and_(FinanceLog.customer_id == cid,
             FinanceLog.stat_date >= start_dt,
             FinanceLog.stat_date <= end_dt))
    if aid:
        q = q.filter(FinanceLog.douyin_account_id == aid)
    q = q.group_by(func.date(FinanceLog.stat_date))
    m = {str(r.d): r for r in q.all()}

    out, cur, run = [], dfrom, 0.0
    while cur <= dto:
        k = cur.isoformat()
        r = m.get(k)
        c = float(r.consume) if r else 0.0
        rc = float(r.recharge) if r else 0.0
        run += rc - c
        out.append({"date": k, "consume": c, "recharge": rc, "balance": round(run, 2)})
        cur += timedelta(days=1)
    return out


def get_accounts(db: Session, cid: int) -> List[DouyinAccount]:
    return (db.query(DouyinAccount)
            .filter(DouyinAccount.customer_id == cid, DouyinAccount.status == "NORMAL")
            .order_by(DouyinAccount.created_at.asc()).all())


def update_douyin_balance(db: Session, aid: int, change: float, log_type: str, remark: str = ""):
    acc = db.query(DouyinAccount).filter(DouyinAccount.id == aid).first()
    if not acc:
        raise ValueError("account not found")
    acc.balance = round(float(acc.balance) + change, 2)
    log = FinanceLog(customer_id=acc.customer_id, douyin_account_id=aid,
                     change_type=log_type, amount=change, balance_after=acc.balance,
                     stat_date=datetime.utcnow(), remark=remark)
    db.add(log)
    db.commit()
    db.refresh(acc)
    return acc