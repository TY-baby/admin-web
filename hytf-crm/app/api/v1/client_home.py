from datetime import date, datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_current_client, get_db
from app.schemas.common import ok, fail
from app.schemas.customer import LaunchReq
from app.services.customer_service import get_client_accounts, launch_delivery
from app.services.douyin_service import get_home_summary, get_trend
from app.services.novel_service import launch_novel, page_link
from app.utils.id_generator import LAUNCH_TYPE_LABEL

router = APIRouter()


@router.get("/accounts")
def accounts(db: Session = Depends(get_db), user=Depends(get_current_client)):
    cid = int(user["sub"])
    accs = get_client_accounts(db, cid)
    return ok([{"id": a.id, "platform_code": a.platform_code,
                "douyin_id": a.douyin_id, "douyin_name": a.douyin_name,
                "auto_code": a.auto_code, "nickname": a.nickname, "tier": a.tier,
                "tier_daily_budget": a.tier_daily_budget,
                "launch_type": a.launch_type,
                "launch_type_label": LAUNCH_TYPE_LABEL.get(a.launch_type, "") if a.launch_type else "",
                "daily_budget": float(a.daily_budget or 0),
                "launch_consumed": float(a.launch_consumed or 0),
                "launch_at": a.launch_at,
                "recharge_amount": float(a.recharge_amount),
                "balance": float(a.balance)}
               for a in accs])


@router.post("/launch")
def launch_api(body: LaunchReq,
               db: Session = Depends(get_db), user=Depends(get_current_client)):
    """首充一键投放"""
    cid = int(user["sub"])
    try:
        acc, consumed, generated = launch_delivery(db, cid, body.platform_code,
                                                   body.douyin_id, body.tier, body.daily_budget)
        return ok({"id": acc.id, "tier": acc.tier, "launch_at": acc.launch_at,
                   "consumed": consumed, "generated": generated,
                   "remaining": float(acc.balance)})
    except ValueError as e:
        return fail(str(e), code=40402)


@router.post("/novel/launch")
def novel_launch_api(body: LaunchReq,
                     db: Session = Depends(get_db), user=Depends(get_current_client)):
    """直播曝光度一键投放（1h内曝光）"""
    cid = int(user["sub"])
    try:
        page, acc, consumed, generated, exposure, remaining = launch_novel(
            db, cid, body.platform_code, body.douyin_id, body.tier, body.daily_budget)
        return ok({"id": page.id, "page_code": page.page_code, "link": page_link(page),
                   "consumed": consumed, "generated": generated,
                   "exposure_1h": exposure, "remaining": remaining})
    except ValueError as e:
        return fail(str(e), code=40402)


@router.get("/summary")
def summary(db: Session = Depends(get_db), user=Depends(get_current_client)):
    return ok(get_home_summary(db, int(user["sub"])))


@router.get("/trend")
def trend(start: Optional[date] = None, end: Optional[date] = None,
          account_id: Optional[int] = None,
          db: Session = Depends(get_db), user=Depends(get_current_client)):
    cid = int(user["sub"])
    # 投放当天不可查数据：查询区间强制截止到昨天
    yesterday = date.today() - timedelta(days=1)
    end = min(end or yesterday, yesterday)
    start = min(start or end, end)
    if (end - start).days > 92:
        end = start + timedelta(days=92)
    return ok({"start": start.isoformat(), "end": end.isoformat(),
               "items": get_trend(db, cid, account_id, start, end)})