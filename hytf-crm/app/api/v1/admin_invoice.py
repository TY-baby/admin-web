from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.schemas.common import fail, ok
from app.schemas.invoice import InvoiceCreateReq
from app.services.invoice_service import create_invoice, list_invoices, process_invoice

router = APIRouter()


@router.get("/list")
def list_api(status: Optional[str] = None,
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    items, total = list_invoices(db, page, page_size, status)
    return ok({"total": total, "page": page, "page_size": page_size,
               "items": [{"id": i.id, "customer_id": i.customer_id,
                          "customer_name": i.customer_name, "amount": float(i.amount),
                          "status": i.status, "invoice_at": i.invoice_at,
                          "processed_at": i.processed_at, "remark": i.remark} for i in items]})


@router.post("/create")
def create_api(body: InvoiceCreateReq,
               db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    return ok({"id": create_invoice(db, body).id})


@router.post("/{iid}/process")
def process_api(iid: int, db: Session = Depends(get_db), _a=Depends(get_current_admin)):
    try:
        inv = process_invoice(db, iid)
        return ok({"id": inv.id, "status": inv.status})
    except ValueError as e:
        return fail(str(e), code=40002)