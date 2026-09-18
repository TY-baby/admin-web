from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_current_client, get_db
from app.models.customer import Customer
from app.schemas.common import ok, fail
from app.schemas.invoice import InvoiceApplyReq, InvoiceCreateReq
from app.services.invoice_service import create_invoice, list_invoices_by_customer

router = APIRouter()


@router.post("/apply")
def apply_api(body: InvoiceApplyReq,
              db: Session = Depends(get_db), user=Depends(get_current_client)):
    cid = int(user["sub"])
    cust = db.query(Customer).filter(Customer.id == cid).first()
    if not cust:
        return fail("客户不存在", code=40401)
    req = InvoiceCreateReq(customer_id=cid, customer_name=cust.customer_name,
                           amount=body.amount, remark=body.remark)
    inv = create_invoice(db, req)
    return ok({"id": inv.id})


@router.get("/list")
def list_api(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
             db: Session = Depends(get_db), user=Depends(get_current_client)):
    cid = int(user["sub"])
    items, total = list_invoices_by_customer(db, cid, page, page_size)
    return ok({"total": total, "page": page, "page_size": page_size,
               "items": [{"id": i.id, "amount": float(i.amount), "status": i.status,
                          "invoice_at": i.invoice_at, "processed_at": i.processed_at,
                          "remark": i.remark} for i in items]})
