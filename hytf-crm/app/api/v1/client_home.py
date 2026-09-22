from datetime import date, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_current_client, get_db
from app.schemas.common import ok, fail
from app.schemas.customer import LaunchReq
from app.services.customer_service import get_client_accounts, launch_delivery
from app.services.douyin_service import get_home_summary, get_trend

router = APIRouter()


@router.get("/accounts")
def accounts(db: Session = Depends(get_db), user=Depends(get_current_client)):
    cid = int(user["sub"])
    accs = get_client_accounts(db, cid)
    return ok([{"id": a.id, "douyin_id": a.douyin_id, "douyin_name": a.douyin_name,
                "auto_code": a.auto_code, "nickname": a.nickname, "tier": a.tier,
                "tier_daily_budget": a.tier_daily_budget, "balance": float(a.balance)}
               for a in accs])


@router.post("/launch")
def launch_api(body: LaunchReq,
               db: Session = Depends(get_db), user=Depends(get_current_client)):
    cid = int(user["sub"])
    try:
        acc, consumed = launch_delivery(db, cid, body.douyin_id, body.tier)
        return ok({"id": acc.id, "tier": acc.tier, "launch_at": acc.launch_at,
                   "consumed": consumed, "remaining": float(acc.balance)})
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
    end = end or date.today()
    start = start or end
    if start > end:
        start, end = end, start
    if (end - start).days > 92:
        end = start + timedelta(days=92)
    return ok({"start": start.isoformat(), "end": end.isoformat(),
               "items": get_trend(db, cid, account_id, start, end)})