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
from app.models.novel_promo import NovelPromo
from app.models.payee import Payee
from app.models.platform import Platform
from app.models.withdraw import Withdraw
from app.schemas.common import ok, fail
from app.schemas.withdraw import WithdrawCreateReq
from app.utils.excel_export import export_rows_to_xlsx
from app.utils.id_generator import (LAUNCH_TYPE_LABEL, NOVEL_PROMO_URL_PREFIX, PROMO_CONTENTS,
                                    load_item_batches)
from app.utils.timeutil import now_cn, today_cn

router = APIRouter()


def _quota_stats(db: Session, a: DouyinAccount, lt: str):
    """总生成条数/热度 与 剩余可出款额度（总量 - 历史出款累计）"""
    generated = 0
    heat = 0
    for b in load_item_batches(a.generated_items):
        b_type = b.get("launch_type") or a.launch_type
        if lt and b_type != lt:
            continue
        items = b.get("items") or []
        generated += len(items)
        if b_type == "EXPOSURE":
            heat += sum(int(it.get("value", 0) or 0) for it in items)
    ws = (db.query(Withdraw)
          .filter(Withdraw.douyin_account_id == a.id,
                  Withdraw.launch_type == lt).all())
    used_count = sum(int(w.generated_count or 0) for w in ws)
    used_heat = sum(int(w.heat_value or 0) for w in ws)
    return generated, heat, max(generated - used_count, 0), max(heat - used_heat, 0)


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
    """级联：首充/曝光 → 客户 → 平台 → ID；网文推广 → 客户 → 平台 → 内容"""
    q = db.query(Customer)
    if keyword:
        q = q.filter(Customer.customer_name.like(f"%{keyword}%"))
    custs = q.order_by(Customer.created_at.desc()).limit(500).all()
    cids = [c.id for c in custs]
    pname = {p.code: p.name for p in db.query(Platform).all()}
    acc_map: dict = {}
    novel_map: dict = {}
    if cids:
        accs = (db.query(DouyinAccount)
                .filter(DouyinAccount.customer_id.in_(cids))
                .order_by(DouyinAccount.created_at.asc()).all())
        for a in accs:
            if int(getattr(a, "is_promo_only", 0) or 0) == 1:
                continue
            acc_map.setdefault(a.customer_id, []).append({
                "id": a.id, "douyin_id": a.douyin_id,
                "douyin_name": a.douyin_name, "nickname": a.nickname,
                "platform_code": a.platform_code,
                "platform_name": pname.get(a.platform_code, a.platform_code),
                "launch_type": a.launch_type or "",
                "tier": a.tier or "",
            })
        nps = db.query(NovelPromo).filter(NovelPromo.customer_id.in_(cids)).all()
        for np in nps:
            plat = novel_map.setdefault(np.customer_id, {})
            plat.setdefault(np.platform_code,
                            {"platform_code": np.platform_code,
                             "platform_name": pname.get(np.platform_code, np.platform_code)})
    return ok([{"id": c.id, "customer_name": c.customer_name,
                "accounts": acc_map.get(c.id, []),
                "novel_options": [{"platform_code": v["platform_code"],
                                   "platform_name": v["platform_name"],
                                   "contents": list(PROMO_CONTENTS)}
                                  for v in novel_map.get(c.id, {}).values()]}
               for c in custs])


@router.get("/novel_preview/{customer_id}")
def preview_novel(customer_id: int, platform_code: Optional[str] = None,
                  promo_content: Optional[str] = None,
                  db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    q = db.query(NovelPromo).filter(NovelPromo.customer_id == customer_id)
    if platform_code:
        q = q.filter(NovelPromo.platform_code == platform_code)
    if promo_content:
        q = q.filter(NovelPromo.promo_content == promo_content)
    np = q.first()
    if not np:
        return fail("无网文推广投放数据", code=40404)
    a = db.query(DouyinAccount).filter(DouyinAccount.id == np.account_id).first()
    if not a:
        return fail("投放账号不存在", code=40404)
    _g, _h, remain_count, _rh = _quota_stats(db, a, "NOVEL_PROMO")
    return ok({"douyin_account_id": a.id, "platform_code": np.platform_code,
               "promo_content": np.promo_content, "generated_count": remain_count})


@router.get("/preview/{account_id}")
def preview_amount(account_id: int, launch_type: Optional[str] = None,
                   db: Session = Depends(get_db),
                   _a=Depends(get_current_admin)):
    a = db.query(DouyinAccount).filter(DouyinAccount.id == account_id).first()
    if not a:
        return fail("投放ID不存在", code=40404)
    lt = launch_type or a.launch_type or ""
    generated, heat, remain_count, remain_heat = _quota_stats(db, a, lt)
    # v10: 返回剩余可出款额度；结算金额纯手动输入，不再计算
    return ok({"douyin_account_id": a.id, "douyin_id": a.douyin_id,
               "douyin_name": a.douyin_name, "nickname": a.nickname,
               "platform_code": a.platform_code,
               "launch_type": lt,
               "generated_count": remain_count,
               "heat_value": remain_heat,
               "total_generated": generated,
               "total_heat": heat,
               "payable_amount": 0.0})


@router.post("/create")
def create_withdraw(body: WithdrawCreateReq,
                    db: Session = Depends(get_db),
                    admin=Depends(get_current_admin)):
    if body.launch_type not in ("FIRST_CHARGE", "EXPOSURE", "NOVEL_PROMO"):
        return fail("类型非法", code=40004)
    payee = db.query(Payee).filter(Payee.id == body.payee_id).first()
    if not payee:
        return fail("打款对象不存在", code=40404)
    is_novel = body.launch_type == "NOVEL_PROMO"
    if is_novel:
        if not body.customer_id:
            return fail("网文推广出款需选择客户/平台/内容", code=40004)
        nq = db.query(NovelPromo).filter(NovelPromo.customer_id == body.customer_id)
        if body.platform_code:
            nq = nq.filter(NovelPromo.platform_code == body.platform_code)
        if body.promo_content:
            nq = nq.filter(NovelPromo.promo_content == body.promo_content)
        np = nq.first()
        if not np:
            return fail("无网文推广投放数据", code=40404)
        acc = db.query(DouyinAccount).filter(DouyinAccount.id == np.account_id).first()
        if not acc:
            return fail("投放账号不存在", code=40404)
        platform_code = body.platform_code or np.platform_code or acc.platform_code or ""
    else:
        acc = db.query(DouyinAccount).filter(DouyinAccount.id == body.douyin_account_id).first()
        if not acc:
            return fail("投放ID不存在", code=40404)
        platform_code = acc.platform_code or ""
    cust = db.query(Customer).filter(Customer.id == acc.customer_id).first()
    operator = admin.get("username", "")
    # v10: 剩余可出款额度校验（0 不允许提交，且不能超过剩余）
    _g, _h, remain_count, remain_heat = _quota_stats(db, acc, body.launch_type)
    if body.launch_type in ("FIRST_CHARGE", "NOVEL_PROMO"):
        cnt = int(body.generated_count or 0)
        if remain_count <= 0:
            return fail("该ID剩余可出款条数为0，不允许提交", code=40005)
        if cnt <= 0:
            return fail("生成条数必须大于0", code=40005)
        if cnt > remain_count:
            return fail(f"生成条数不能超过剩余可出款条数（{remain_count}）", code=40005)
    else:
        hv = int(body.heat_value or 0)
        if remain_heat <= 0:
            return fail("该ID曝光度剩余可出款热度为0，不允许提交", code=40005)
        if hv <= 0:
            return fail("热度必须大于0", code=40005)
        if hv > remain_heat:
            return fail(f"热度不能超过剩余可出款热度（{remain_heat}）", code=40005)
    w = Withdraw(
        payee_id=payee.id, payee_card_no=payee.card_no,
        payee_bank_name=payee.bank_name, payee_holder_name=payee.display_name,
        customer_id=cust.id if cust else 0,
        customer_name=cust.customer_name if cust else "",
        douyin_account_id=acc.id,
        douyin_id=(body.promo_content or "") if is_novel else acc.douyin_id,
        douyin_name=(body.promo_content or "") if is_novel else (acc.douyin_name or acc.nickname),
        platform_code=platform_code,
        launch_type=body.launch_type,
        generated_count=int(body.generated_count or 0),
        heat_value=int(body.heat_value or 0),
        payable_amount=float(body.payable_amount),
        settle_date=body.settle_date or today_cn(),
        remark=body.remark, operator=operator,
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    logger.info(f"[withdraw created] id={w.id} payee={payee.display_name} "
                f"account={acc.douyin_id} type={body.launch_type} "
                f"amount={body.payable_amount} settle={w.settle_date} operator={operator}")
    return ok({"id": w.id, "payable_amount": float(w.payable_amount)})


@router.get("/list")
def list_api(keyword: Optional[str] = None,
             launch_type: Optional[str] = None,
             date_from: Optional[date] = None, date_to: Optional[date] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    q = db.query(Withdraw)
    if keyword:
        # 3.1.5：模糊匹配（客户 / 打款对象 / 投放ID / 卡号）
        q = q.filter(
            (Withdraw.payee_holder_name.like(f"%{keyword}%")) |
            (Withdraw.payee_card_no.like(f"%{keyword}%")) |
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
    pname = {p.code: p.name for p in db.query(Platform).all()}
    return ok({"total": total, "page": page, "page_size": page_size,
               "items": [{
                   "id": w.id,
                   "payee_holder_name": w.payee_holder_name,
                   "payee_bank_name": w.payee_bank_name,
                   "payee_card_no": w.payee_card_no,
                   "customer_name": w.customer_name,
                   "douyin_id": w.douyin_id,
                   "douyin_name": w.douyin_name,
                   "platform_code": w.platform_code or "",
                   "platform_name": pname.get(w.platform_code, w.platform_code or ""),
                   "launch_type": w.launch_type or "",
                   "launch_type_label": LAUNCH_TYPE_LABEL.get(w.launch_type, "") if w.launch_type else "",
                   "generated_count": w.generated_count,
                   "heat_value": w.heat_value or 0,
                   "payable_amount": float(w.payable_amount),
                   "settle_date": w.settle_date.strftime("%Y-%m-%d") if w.settle_date else "",
                   "remark": w.remark,
                   "operator": w.operator,
                   "created_at": w.created_at.strftime("%Y-%m-%d %H:%M:%S") if w.created_at else "",
               } for w in rows]})


@router.get("/export")
def export_withdraw(keyword: Optional[str] = None,
                    launch_type: Optional[str] = None,
                    date_from: Optional[date] = None, date_to: Optional[date] = None,
                    db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    """3.1.6：出款管理导出
       字段：打款对象、卡号、类型、结算金额、产出ID、产出昵称、结算日期
       首充 → 按明细展开 biz_code / nickname
       曝光 → 产出ID/产出昵称 位置显示"热度"值"""
    if not launch_type or launch_type not in ("FIRST_CHARGE", "EXPOSURE", "NOVEL_PROMO"):
        return fail("导出前必须先选择类型（首充/曝光度/网文推广）", code=40004)

    q = db.query(Withdraw).filter(Withdraw.launch_type == launch_type)
    if keyword:
        q = q.filter(
            (Withdraw.payee_holder_name.like(f"%{keyword}%")) |
            (Withdraw.customer_name.like(f"%{keyword}%")) |
            (Withdraw.douyin_id.like(f"%{keyword}%"))
        )
    if date_from:
        q = q.filter(Withdraw.settle_date >= date_from)
    if date_to:
        q = q.filter(Withdraw.settle_date <= date_to)
    ws = q.order_by(Withdraw.settle_date.asc(), Withdraw.id.asc()).all()
    if not ws:
        return fail("未匹配到出款记录", code=40404)

    acc_ids = list({w.douyin_account_id for w in ws})
    accs = {a.id: a for a in db.query(DouyinAccount).filter(DouyinAccount.id.in_(acc_ids)).all()}
    type_label = LAUNCH_TYPE_LABEL.get(launch_type, "")
    is_exposure = launch_type == "EXPOSURE"
    is_novel = launch_type == "NOVEL_PROMO"
    if is_novel:
        headers = ["打款对象", "卡号", "类型", "结算金额", "网址", "阅读量", "结算日期"]
    elif is_exposure:
        headers = ["打款对象", "卡号", "类型", "结算金额", "热度", "结算日期"]
    else:
        headers = ["打款对象", "卡号", "类型", "结算金额", "产出ID", "产出昵称", "结算日期"]

    rows = []
    for w in ws:
        a = accs.get(w.douyin_account_id)
        base = [w.payee_holder_name, w.payee_card_no, type_label,
                float(w.payable_amount or 0)]
        settle = w.settle_date.strftime("%Y-%m-%d") if w.settle_date else ""
        if is_exposure:
            rows.append(base + [int(w.heat_value or 0), settle])
            continue
        if is_novel:
            expanded = False
            if a:
                for b in load_item_batches(a.generated_items):
                    if (b.get("launch_type") or a.launch_type) != "NOVEL_PROMO":
                        continue
                    for it in b.get("items") or []:
                        url = NOVEL_PROMO_URL_PREFIX + str(it.get("url_code", ""))
                        rows.append(base + [url, it.get("value", ""), settle])
                        expanded = True
            if not expanded:
                rows.append(base + ["", "", settle])
            continue
        # 首充：展开每条明细的 biz_code + nickname
        expanded = False
        if a:
            for b in load_item_batches(a.generated_items):
                b_type = b.get("launch_type") or a.launch_type
                if b_type != "FIRST_CHARGE":
                    continue
                for it in b.get("items") or []:
                    rows.append(base + [it.get("biz_code", ""), it.get("nickname", ""), settle])
                    expanded = True
        if not expanded:
            rows.append(base + [w.douyin_id, w.douyin_name, settle])

    content = export_rows_to_xlsx(headers, rows)
    fname = f"withdraw_{type_label}_{now_cn().strftime('%Y%m%d%H%M%S')}.xlsx"
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
