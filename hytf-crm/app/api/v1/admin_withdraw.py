from datetime import datetime, date, time
from io import BytesIO
from typing import Optional
from urllib.parse import quote
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.models.platform import Platform
from app.schemas.common import ok, fail
from app.services.customer_service import list_customers, _generated_count
from app.utils.excel_export import export_rows_to_xlsx_merged
from app.utils.id_generator import load_items

router = APIRouter()


def _has_cond(keyword_name, keyword_phone, date_from, date_to) -> bool:
    return bool(keyword_name or keyword_phone or date_from or date_to)


@router.get("/list")
def list_api(keyword_name: Optional[str] = None, keyword_phone: Optional[str] = None,
             date_from: Optional[date] = None, date_to: Optional[date] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    """出款管理列表：数据源来自客户管理（按客户聚合）"""
    df = datetime.combine(date_from, time.min) if date_from else None
    dt = datetime.combine(date_to, time.max) if date_to else None
    items, total = list_customers(db, keyword_name, None, df, dt, page, page_size,
                                  phone=keyword_phone)
    rows = []
    for c in items:
        dl = getattr(c, "douyin_list", []) or []
        id_count = sum(_generated_count(a) for a in dl)
        total_recharge = round(sum(float(a.recharge_amount or 0) for a in dl), 2)
        rows.append({
            "id": c.id, "customer_uid": c.customer_uid, "customer_name": c.customer_name,
            "contact_name": c.contact_name, "phone": c.phone,
            # 打款日期 = 添加客户时间
            "pay_date": c.created_at.strftime("%Y-%m-%d") if c.created_at else "",
            "created_at": c.created_at,
            "id_count": id_count, "total_recharge": total_recharge,
        })
    return ok({"total": total, "page": page, "page_size": page_size, "items": rows})


@router.get("/export")
def export_api(keyword_name: Optional[str] = None, keyword_phone: Optional[str] = None,
               date_from: Optional[date] = None, date_to: Optional[date] = None,
               db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    """出款导出：内容与用户管理导出一致，但取消 日预算/1h曝光度/类型/授权开始 字段"""
    if not _has_cond(keyword_name, keyword_phone, date_from, date_to):
        return fail("必须先输入查询条件进行导出", code=40003)
    df = datetime.combine(date_from, time.min) if date_from else None
    dt = datetime.combine(date_to, time.max) if date_to else None
    items, _ = list_customers(db, keyword_name, None, df, dt, 1, 10000, phone=keyword_phone)
    pname = {p.code: p.name for p in db.query(Platform).all()}
    headers = ["客户UID", "客户名称", "联系人", "手机号", "投放ID", "名称",
               "投放平台名称", "总充值金额", "档位", "ID", "昵称", "投放日期"]
    rows, merge_groups = [], []
    for c in items:
        group_start = len(rows)
        dl = getattr(c, "douyin_list", []) or []
        if not dl:
            rows.append([c.customer_uid, c.customer_name, c.contact_name, c.phone,
                         "", "", "", "", "", "", "", ""])
        for a in dl:
            launch_date = a.launch_at.strftime("%Y-%m-%d") if a.launch_at else ""
            base = [c.customer_uid, c.customer_name, c.contact_name, c.phone,
                    a.douyin_id, a.douyin_name,
                    pname.get(a.platform_code, a.platform_code),
                    float(a.recharge_amount)]
            stored = load_items(a.generated_items)
            if not (a.tier and a.launch_at) or not stored:
                rows.append(base + [a.tier or "-", "-", "-", launch_date])
                continue
            for it in stored:
                rows.append(base + [a.tier, it.get("biz_code", ""),
                                    it.get("nickname", ""), launch_date])
        if len(rows) - 1 >= group_start:
            merge_groups.append((group_start, len(rows) - 1))
    content = export_rows_to_xlsx_merged(headers, rows, merge_groups, (0, 1, 2, 3))
    fname = f"withdraw_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    return StreamingResponse(BytesIO(content),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(fname)}"})
