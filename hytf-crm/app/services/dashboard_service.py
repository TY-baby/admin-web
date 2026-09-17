from datetime import datetime, timedelta, date
from sqlalchemy import func, and_, case
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.models.douyin_account import DouyinAccount
from app.models.finance_log import FinanceLog
from app.models.invoice import Invoice


def admin_dashboard(db: Session, days: int = 14) -> dict:
    total_customer = db.query(func.count(Customer.id)).scalar() or 0
    total_douyin = db.query(func.count(DouyinAccount.id)).scalar() or 0
    total_recharge = db.query(func.coalesce(func.sum(DouyinAccount.recharge_amount), 0)).scalar() or 0
    total_consume = db.query(func.coalesce(func.sum(-FinanceLog.amount), 0)).filter(
        FinanceLog.change_type == "CONSUME").scalar() or 0

    now = datetime.utcnow()
    expiring = db.query(func.count(DouyinAccount.id)).filter(and_(
        DouyinAccount.auth_end_at.isnot(None),
        DouyinAccount.auth_end_at > now,
        DouyinAccount.auth_end_at <= now + timedelta(days=3),
        DouyinAccount.status == "NORMAL")).scalar() or 0
    expired = db.query(func.count(DouyinAccount.id)).filter(and_(
        DouyinAccount.auth_end_at.isnot(None),
        DouyinAccount.auth_end_at <= now)).scalar() or 0
    inv_pending = db.query(func.count(Invoice.id)).filter(Invoice.status == "PENDING").scalar() or 0

    start_d = date.today() - timedelta(days=days - 1)
    consume_expr = func.coalesce(func.sum(case((FinanceLog.change_type == "CONSUME", -FinanceLog.amount), else_=0)), 0)
    recharge_expr = func.coalesce(func.sum(case((FinanceLog.change_type == "RECHARGE", FinanceLog.amount), else_=0)), 0)
    rows = db.query(func.date(FinanceLog.stat_date).label("d"),
                    consume_expr.label("consume"),
                    recharge_expr.label("recharge")).filter(
        FinanceLog.stat_date >= datetime.combine(start_d, datetime.min.time())
    ).group_by(func.date(FinanceLog.stat_date)).all()
    m = {str(r.d): r for r in rows}

    trend, cur, bal = [], start_d, 0.0
    while cur <= date.today():
        r = m.get(cur.isoformat())
        c = float(r.consume) if r else 0.0
        rc = float(r.recharge) if r else 0.0
        bal += rc - c
        trend.append({"date": cur.isoformat(), "consume": c, "recharge": rc, "balance": round(bal, 2)})
        cur += timedelta(days=1)

    return {"total_customer": int(total_customer), "total_douyin": int(total_douyin),
            "total_recharge": float(total_recharge), "total_consume": float(total_consume),
            "expiring_count": int(expiring), "expired_count": int(expired),
            "invoice_pending": int(inv_pending), "trend": trend}