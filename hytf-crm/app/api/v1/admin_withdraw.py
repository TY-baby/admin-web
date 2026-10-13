from datetime import datetime, date, time
from io import BytesIO
from typing import Optional
from urllib.parse import quote
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.core.logging_conf import logger
from app.models.customer import Customer
from app.models.douyin_account import DouyinAccount
from app.models.payee import Payee
from app.models.platform import Platform
from app.models.withdraw import Withdraw
from app.schemas.common import ok, fail
from app.schemas.withdraw import WithdrawCreateReq
from app.utils.excel_export import export_rows_to_xlsx_merged
from app.utils.id_generator import (EXPOSURE_TIER_PRICE, LAUNCH_TYPE_LABEL,
                                    TIER_DAILY_BUDGET, load_item_batches, load_items)

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
        launch_type=acc.launch_type or "",
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
             launch_type: Optional[str] = None,
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
    if launch_type:
        q = q.filter(Withdraw.launch_type == launch_type)
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
                   "launch_type": w.launch_type or "",
                   "launch_type_label": LAUNCH_TYPE_LABEL.get(w.launch_type, "") if w.launch_type else "",
                   "generated_count": w.generated_count,
                   "payable_amount": float(w.payable_amount),
                   "remark": w.remark,
                   "operator": w.operator,
                   "created_at": w.created_at.strftime("%Y-%m-%d %H:%M:%S") if w.created_at else "",
               } for w in rows]})


@router.get("/export")
def export_withdraw(keyword: Optional[str] = None,
                    launch_type: Optional[str] = None,
                    db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    """需求 4.2：出款管理导出 Excel
       - 必须选择类型（首充/曝光度）
       - 必须输入关键词（限定为一个客户）
       - 字段与用户管理导出一致"""
    if not launch_type or launch_type not in ("FIRST_CHARGE", "EXPOSURE"):
        return fail("导出前必须先选择类型（首充/曝光度）", code=40004)
    if not keyword:
        return fail("导出前必须输入关键词，且只能导出一个客户的数据", code=40003)

    ws = (db.query(Withdraw)
          .filter(Withdraw.launch_type == launch_type)
          .filter(Withdraw.customer_name.like(f"%{keyword}%"))
          .order_by(Withdraw.created_at.asc()).all())
    if not ws:
        return fail("未匹配到该客户的出款记录", code=40404)
    cust_ids = {w.customer_id for w in ws}
    if len(cust_ids) > 1:
        return fail("关键词命中多个客户，请精确到唯一客户后再导出", code=40003)

    acc_ids = [w.douyin_account_id for w in ws]
    accs = {a.id: a for a in db.query(DouyinAccount).filter(DouyinAccount.id.in_(acc_ids)).all()}
    cust = db.query(Customer).filter(Customer.id == list(cust_ids)[0]).first()
    pname = {p.code: p.name for p in db.query(Platform).all()}

    is_exposure = launch_type == "EXPOSURE"
    value_col = "1h曝光度" if is_exposure else "总充值金额"
    headers = ["客户UID", "客户名称", "联系人", "手机号", "投放ID", "名称",
               "投放平台名称", "消耗金额", "档位", "ID", "昵称",
               value_col, "类型", "投放日期"]
    type_label = LAUNCH_TYPE_LABEL.get(launch_type, "")
    rows = []
    merge_groups = []
    for w in ws:
        a = accs.get(w.douyin_account_id)
        if not a:
            continue
        group_start = len(rows)
        base = [cust.customer_uid if cust else "", cust.customer_name if cust else w.customer_name,
                cust.contact_name if cust else "", cust.phone if cust else "",
                a.douyin_id, a.douyin_name, pname.get(a.platform_code, a.platform_code)]
        batches = load_item_batches(a.generated_items)
        if not batches:
            rows.append(base + ["", "-", "-", "-", "", ""])
            continue
        for b in batches:
            b_tier = b.get("tier") or a.tier
            b_type = b.get("launch_type") or a.launch_type
            if b_type != launch_type:
                continue
            b_consumed = b.get("consumed")
            if b_consumed is None:
                price_map = EXPOSURE_TIER_PRICE if b_type == "EXPOSURE" else TIER_DAILY_BUDGET
                b_consumed = round(len(b["items"]) * price_map.get(b_tier, 0), 2)
            ld = (b.get("launch_at") or "")[:10]
            for it in b["items"]:
                rows.append(base + [float(b_consumed), b_tier,
                                    it.get("biz_code", ""), it.get("nickname", ""),
                                    it.get("value", ""), type_label, ld])
        if len(rows) - 1 >= group_start:
            merge_groups.append((group_start, len(rows) - 1))

    content = export_rows_to_xlsx_merged(headers, rows, merge_groups, (0, 1, 2, 3))
    fname = f"withdraw_{type_label}_{keyword}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    return StreamingResponse(BytesIO(content),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(fname)}"})


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
