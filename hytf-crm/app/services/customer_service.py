from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.core.logging_conf import logger
from app.core.security import build_client_default_password, hash_password
from app.models.customer import Customer
from app.models.douyin_account import DouyinAccount
from app.models.finance_log import FinanceLog
from app.models.platform import Platform
from app.schemas.customer import CustomerCreateReq, CustomerUpdateReq, DouyinUpdateReq
from app.utils.id_generator import (EXPOSURE_TIER_PRICE, EXPOSURE_TIER_RANGE, LAUNCH_TYPE_LABEL,
                                    TIER_DAILY_BUDGET, TIER_ITEM_RANGE,
                                    dump_items, gen_auto_code, gen_customer_uid,
                                    gen_launch_items, gen_nickname, load_items)

AUTH_DAYS = {"D3": 3, "D7": 7, "D30": 30}


def _calc_end(duration: str, custom_days: Optional[int], start: datetime):
    if duration == "UNLIMITED":
        return None
    if duration == "CUSTOM":
        if not custom_days:
            raise ValueError("custom auth requires auth_days_custom")
        return start + timedelta(days=custom_days)
    return start + timedelta(days=AUTH_DAYS[duration])


def _status_label(a: DouyinAccount) -> str:
    if a.status == "DISABLED":
        return "禁用"
    if a.auth_end_at is None:
        return "正常"
    now = datetime.utcnow()
    if a.auth_end_at <= now:
        return "已到期"
    if (a.auth_end_at - now).days <= 3:
        return "即将到期"
    return "正常"


def _remain_after_consume(a: DouyinAccount) -> float:
    # 修复：直接返回数据库真实余额（追加充值时已同步更新 balance）
    # 投放时 launch_delivery/launch_novel 已把 consumed 从 balance 中扣减
    return float(a.balance or 0)


def _generated_count(a: DouyinAccount) -> int:
    """已生成的 ID 条数：优先从落库的 generated_items 读取，历史数据回退计算"""
    items = load_items(a.generated_items)
    if items:
        return len(items)
    if a.tier and a.launch_at and a.daily_budget:
        price = (EXPOSURE_TIER_PRICE if a.launch_type == "EXPOSURE" else TIER_DAILY_BUDGET).get(a.tier)
        if price:
            return max(1, int(float(a.daily_budget) // price))
    return 0


def list_customers(db: Session, name=None, dyid=None, dfrom=None, dto=None,
                   page: int = 1, size: int = 20, only_ids=None,
                   launch_type: Optional[str] = None,
                   phone: Optional[str] = None) -> Tuple[List[Customer], int]:
    q = db.query(Customer)
    if only_ids is not None:
        q = q.filter(Customer.id.in_(only_ids))
    if name:
        q = q.filter(Customer.customer_name.like(f"%{name}%"))
    if phone:
        q = q.filter(Customer.phone.like(f"%{phone}%"))
    if dfrom:
        q = q.filter(Customer.created_at >= dfrom)
    if dto:
        q = q.filter(Customer.created_at <= dto)
    if dyid:
        sub = db.query(DouyinAccount.customer_id).filter(
            DouyinAccount.douyin_id.like(f"%{dyid}%")).subquery()
        q = q.filter(Customer.id.in_(sub))
    if launch_type:
        sub = db.query(DouyinAccount.customer_id).filter(
            DouyinAccount.launch_type == launch_type).subquery()
        q = q.filter(Customer.id.in_(sub))
    total = q.count()
    items = q.order_by(Customer.created_at.desc()).offset((page - 1) * size).limit(size).all()
    ids = [c.id for c in items]
    if ids:
        m = {}
        acc_q = db.query(DouyinAccount).filter(DouyinAccount.customer_id.in_(ids))
        if launch_type:
            acc_q = acc_q.filter(DouyinAccount.launch_type == launch_type)
        accs = acc_q.order_by(DouyinAccount.created_at.asc()).all()
        for a in accs:
            m.setdefault(a.customer_id, []).append(a)
        for c in items:
            c.douyin_list = m.get(c.id, [])
    return items, total


def create_customer(db: Session, req: CustomerCreateReq) -> Customer:
    cust = db.query(Customer).filter(Customer.phone == req.phone).first()
    if cust is None:
        uids = {u for (u,) in db.query(Customer.customer_uid).all()}
        cust = Customer(customer_uid=gen_customer_uid(uids),
                        customer_name=req.customer_name,
                        contact_name=req.contact_name,
                        phone=req.phone,
                        password_hash=hash_password(build_client_default_password(req.phone)),
                        remark=req.remark)
        db.add(cust)
        db.flush()
        logger.info(f"[customer created] uid={cust.customer_uid} phone={req.phone}")
    else:
        cust.customer_name = req.customer_name or cust.customer_name
        cust.contact_name = req.contact_name or cust.contact_name

    codes = {c for (c,) in db.query(DouyinAccount.auto_code).all()}
    exists = {(p, i) for p, i in db.query(DouyinAccount.platform_code, DouyinAccount.douyin_id).all()}
    platforms = {c for (c,) in db.query(Platform.code).all()}

    for d in req.douyin_list:
        pcode = d.platform_code or "douyin"
        if platforms and pcode not in platforms:
            raise ValueError(f"投放平台不存在: {pcode}")
        if (pcode, d.douyin_id) in exists:
            raise ValueError(f"该平台下ID已存在: {d.douyin_id}")
        start = datetime.utcnow()
        acc = DouyinAccount(customer_id=cust.id, platform_code=pcode,
                            douyin_id=d.douyin_id,
                            douyin_name=d.douyin_name,
                            auto_code=gen_auto_code(codes), nickname=gen_nickname(),
                            recharge_amount=d.recharge_amount, balance=d.recharge_amount,
                            tier=None, tier_daily_budget=0,
                            auth_duration=d.auth_duration, auth_start_at=start,
                            auth_end_at=_calc_end(d.auth_duration, d.auth_days_custom, start),
                            status="NORMAL", remark=d.remark)
        codes.add(acc.auto_code)
        exists.add((pcode, d.douyin_id))
        db.add(acc)
        db.flush()
        db.add(FinanceLog(customer_id=cust.id, douyin_account_id=acc.id,
                          change_type="RECHARGE", amount=d.recharge_amount,
                          balance_after=d.recharge_amount, stat_date=start,
                          remark="管理员录入充值"))
    db.commit()
    db.refresh(cust)
    return cust


def update_customer(db: Session, cid: int, req: CustomerUpdateReq) -> Customer:
    c = db.query(Customer).filter(Customer.id == cid).first()
    if not c:
        raise ValueError("customer not found")
    if req.customer_name is not None: c.customer_name = req.customer_name
    if req.contact_name is not None: c.contact_name = req.contact_name
    if req.remark is not None: c.remark = req.remark
    if req.is_active is not None: c.is_active = req.is_active
    db.commit()
    db.refresh(c)
    return c


def update_douyin(db: Session, aid: int, req: DouyinUpdateReq) -> DouyinAccount:
    a = db.query(DouyinAccount).filter(DouyinAccount.id == aid).first()
    if not a:
        raise ValueError("douyin account not found")
    if req.douyin_name is not None: a.douyin_name = req.douyin_name
    # 充值金额为追加逻辑：录入多少累加多少
    if req.recharge_amount is not None and req.recharge_amount > 0:
        add = float(req.recharge_amount)
        a.recharge_amount = round(float(a.recharge_amount) + add, 2)
        a.balance = round(float(a.balance) + add, 2)
        db.add(FinanceLog(customer_id=a.customer_id, douyin_account_id=a.id,
                          change_type="RECHARGE", amount=add, balance_after=a.balance,
                          stat_date=datetime.utcnow(), remark="管理员追加充值"))
    if req.auth_duration is not None:
        a.auth_duration = req.auth_duration
        a.auth_end_at = _calc_end(req.auth_duration, req.auth_days_custom, a.auth_start_at)
    if req.status is not None: a.status = req.status
    if req.remark is not None: a.remark = req.remark
    db.commit()
    db.refresh(a)
    return a


def launch_delivery(db: Session, cid: int, platform_code: str, douyin_id: str,
                    tier: str, daily_budget: float):
    """首充一键投放：生成条数 = floor(日预算/档位金额)，消耗 = 条数 * 档位金额
       同时一次性生成 ID/昵称/单条金额并落库，保证后续导出数据稳定"""
    a = db.query(DouyinAccount).filter(DouyinAccount.customer_id == cid,
                                       DouyinAccount.platform_code == platform_code,
                                       DouyinAccount.douyin_id == douyin_id).first()
    if not a:
        raise ValueError("投放ID不存在或不属于当前客户")
    price = TIER_DAILY_BUDGET[tier]
    if daily_budget < price:
        raise ValueError("日预算不能小于所选档位金额")
    balance = float(a.balance)
    if balance < daily_budget:
        raise ValueError("日预算不能超过当前账号余额")
    generated = int(daily_budget // price)
    consumed = round(generated * price, 2)
    remaining = round(balance - consumed, 2)
    # 关键：一次性生成随机明细并落库（保证多次导出结果一致）
    items = gen_launch_items(generated, TIER_ITEM_RANGE[tier])
    a.tier = tier
    a.tier_daily_budget = price
    a.launch_type = "FIRST_CHARGE"
    a.daily_budget = daily_budget
    a.launch_consumed = consumed
    a.generated_items = dump_items(items)
    a.launch_at = datetime.utcnow()
    a.balance = remaining
    db.add(FinanceLog(customer_id=a.customer_id, douyin_account_id=a.id,
                      change_type="CONSUME", amount=-consumed,
                      balance_after=remaining, stat_date=datetime.utcnow(),
                      remark=f"首充一键投放结算(生成{generated}条)"))
    db.commit()
    db.refresh(a)
    return a, consumed, generated


def delete_customer(db: Session, cid: int) -> None:
    c = db.query(Customer).filter(Customer.id == cid).first()
    if not c:
        return
    db.query(DouyinAccount).filter(DouyinAccount.customer_id == cid).delete()
    db.query(FinanceLog).filter(FinanceLog.customer_id == cid).delete()
    db.delete(c)
    db.commit()


def delete_douyin(db: Session, aid: int) -> None:
    a = db.query(DouyinAccount).filter(DouyinAccount.id == aid).first()
    if not a:
        return
    db.query(FinanceLog).filter(FinanceLog.douyin_account_id == aid).delete()
    db.delete(a)
    db.commit()


def to_customer_item(c: Customer) -> dict:
    return {
        "id": c.id, "customer_uid": c.customer_uid, "customer_name": c.customer_name,
        "contact_name": c.contact_name, "phone": c.phone, "is_active": c.is_active,
        "remark": c.remark, "created_at": c.created_at,
        "douyin_list": [{
            "id": a.id, "platform_code": a.platform_code,
            "douyin_id": a.douyin_id, "douyin_name": a.douyin_name,
            "auto_code": a.auto_code, "nickname": a.nickname,
            "recharge_amount": float(a.recharge_amount),
            "balance": _remain_after_consume(a),
            "tier": a.tier, "tier_daily_budget": a.tier_daily_budget,
            "launch_type": a.launch_type,
            "launch_type_label": LAUNCH_TYPE_LABEL.get(a.launch_type, "") if a.launch_type else "",
            "daily_budget": float(a.daily_budget or 0),
            "launch_consumed": float(a.launch_consumed or 0),
            "generated_count": _generated_count(a),
            "exposure_1h": int(a.exposure_1h or 0),
            "launch_at": a.launch_at,
            "auth_duration": a.auth_duration, "auth_start_at": a.auth_start_at,
            "auth_end_at": a.auth_end_at, "status": a.status,
            "status_label": _status_label(a), "remark": a.remark,
            "created_at": a.created_at,
        } for a in (getattr(c, "douyin_list", []) or [])],
    }


def get_client_accounts(db: Session, cid: int) -> List[DouyinAccount]:
    return (db.query(DouyinAccount)
            .filter(DouyinAccount.customer_id == cid, DouyinAccount.status == "NORMAL")
            .order_by(DouyinAccount.created_at.asc()).all())
