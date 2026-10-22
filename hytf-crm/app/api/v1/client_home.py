from datetime import date, datetime, timedelta
from io import BytesIO
from typing import Optional
from urllib.parse import quote
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.deps import get_current_client, get_db
from app.models.douyin_account import DouyinAccount
from app.models.platform import Platform
from app.schemas.common import ok, fail
from app.schemas.customer import LaunchReq, NovelPromoLaunchReq
from app.services.customer_service import calc_total_consumed, get_client_accounts, launch_delivery
from app.services.douyin_service import get_home_summary, get_launch_stats, get_trend
from app.services.novel_service import launch_novel, launch_novel_promo, page_link
from app.utils.excel_export import export_rows_to_xlsx
from app.utils.id_generator import (LAUNCH_TYPE_LABEL, NOVEL_PROMO_URL_PREFIX,
                                    gen_recharge_order_no, load_item_batches)
from app.utils.timeutil import today_cn

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
                "total_consumed": calc_total_consumed(a),
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


@router.post("/novel_promo/launch")
def novel_promo_launch_api(body: NovelPromoLaunchReq,
                           db: Session = Depends(get_db), user=Depends(get_current_client)):
    """网文推广一键投放（投放内容 + 档位 + 预算，无投放ID）"""
    cid = int(user["sub"])
    try:
        acc, consumed, generated, reads_total, remaining = launch_novel_promo(
            db, cid, body.platform_code, body.promo_content, body.tier, body.daily_budget)
        return ok({"id": acc.id, "consumed": consumed, "generated": generated,
                   "reads_total": reads_total, "remaining": remaining})
    except ValueError as e:
        return fail(str(e), code=40402)


@router.get("/summary")
def summary(db: Session = Depends(get_db), user=Depends(get_current_client)):
    return ok(get_home_summary(db, int(user["sub"])))


@router.get("/trend")
def trend(start: Optional[date] = None, end: Optional[date] = None,
          account_id: Optional[int] = None,
          launch_type: Optional[str] = None,
          db: Session = Depends(get_db), user=Depends(get_current_client)):
    cid = int(user["sub"])
    yesterday = today_cn() - timedelta(days=1)
    end = min(end or yesterday, yesterday)
    start = min(start or end, end)
    if (end - start).days > 92:
        end = start + timedelta(days=92)
    items = get_trend(db, cid, account_id, start, end)
    stats = None
    if launch_type in ("FIRST_CHARGE", "EXPOSURE", "NOVEL_PROMO"):
        stats = get_launch_stats(db, cid, account_id, launch_type, start, end)
    return ok({"start": start.isoformat(), "end": end.isoformat(),
               "items": items, "stats": stats})


@router.get("/export")
def export_api(start: Optional[date] = None, end: Optional[date] = None,
               account_id: Optional[int] = None,
               launch_type: Optional[str] = None,
               db: Session = Depends(get_db), user=Depends(get_current_client)):
    """A端流水明细导出。网文推广为客户级（无需选ID），首充/曝光度需选ID。"""
    cid = int(user["sub"])
    if not launch_type or launch_type not in ("FIRST_CHARGE", "EXPOSURE", "NOVEL_PROMO"):
        return fail("导出前必须选择类型（首充/直播曝光度/网文推广）", code=40004)
    yesterday = today_cn() - timedelta(days=1)
    end = min(end or yesterday, yesterday)
    start = min(start or end, end)
    pname = {p.code: p.name for p in db.query(Platform).all()}
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    if launch_type == "NOVEL_PROMO":
        headers = ["投放平台", "投放内容", "类型", "档位", "网址", "阅读量", "投放日期"]
        rows = []
        accs = db.query(DouyinAccount).filter(DouyinAccount.customer_id == cid).all()
        for acc in accs:
            for b in load_item_batches(acc.generated_items):
                if (b.get("launch_type") or acc.launch_type) != "NOVEL_PROMO":
                    continue
                ld = (b.get("launch_at") or "")[:10]
                if not ld or not (start_str <= ld <= end_str):
                    continue
                b_tier = b.get("tier") or acc.tier or "-"
                for it in b.get("items") or []:
                    url = NOVEL_PROMO_URL_PREFIX + str(it.get("url_code", ""))
                    rows.append([pname.get(acc.platform_code, acc.platform_code),
                                 it.get("promo_content", ""), "网文推广", b_tier,
                                 url, it.get("value", ""), ld])
        content = export_rows_to_xlsx(headers, rows)
        fname = f"流水明细_网文推广_{start.isoformat()}_{end.isoformat()}.xlsx"
        return StreamingResponse(BytesIO(content),
                                 media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(fname)}"})

    if not account_id:
        return fail("导出前必须选择投放ID", code=40004)
    acc = (db.query(DouyinAccount)
           .filter(DouyinAccount.id == account_id,
                   DouyinAccount.customer_id == cid).first())
    if not acc:
        return fail("投放ID不存在或不属于当前客户", code=40404)

    is_first = launch_type == "FIRST_CHARGE"
    value_col = "首充金额" if is_first else "直播热度"
    headers = ["投放平台名称", "投放ID", "档位", "类型"]
    if is_first:
        headers += ["ID", "昵称"]
    headers += [value_col, "投放日期", "充值订单号"]

    rows = []
    for b in load_item_batches(acc.generated_items):
        b_type = b.get("launch_type") or acc.launch_type
        if b_type != launch_type:
            continue
        ld = (b.get("launch_at") or "")[:10]
        if not ld or not (start_str <= ld <= end_str):
            continue
        b_tier = b.get("tier") or acc.tier or "-"
        b_type_label = LAUNCH_TYPE_LABEL.get(b_type, "")
        for it in b.get("items") or []:
            row = [pname.get(acc.platform_code, acc.platform_code),
                   acc.douyin_id, b_tier, b_type_label]
            if is_first:
                row += [it.get("biz_code", ""), it.get("nickname", "")]
            row += [it.get("value", ""), ld, gen_recharge_order_no()]
            rows.append(row)

    content = export_rows_to_xlsx(headers, rows)
    type_label = LAUNCH_TYPE_LABEL.get(launch_type, "")
    fname = f"launch_{type_label}_{acc.douyin_id}_{start.isoformat()}_{end.isoformat()}.xlsx"
    return StreamingResponse(BytesIO(content),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(fname)}"})
