from datetime import datetime
from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreateReq


def list_invoices(db: Session, page=1, size=20, status=None):
    q = db.query(Invoice)
    if status:
        q = q.filter(Invoice.status == status)
    total = q.count()
    items = q.order_by(Invoice.invoice_at.desc()).offset((page - 1) * size).limit(size).all()
    return items, total


def list_invoices_by_customer(db: Session, customer_id: int, page=1, size=20):
    q = db.query(Invoice).filter(Invoice.customer_id == customer_id)
    total = q.count()
    items = q.order_by(Invoice.invoice_at.desc()).offset((page - 1) * size).limit(size).all()
    return items, total


def create_invoice(db: Session, req: InvoiceCreateReq) -> Invoice:
    inv = Invoice(customer_id=req.customer_id, customer_name=req.customer_name,
                  douyin_id=req.douyin_id,
                  amount=req.amount, remark=req.remark, status="PENDING",
                  invoice_at=datetime.utcnow())
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv


def process_invoice(db: Session, iid: int) -> Invoice:
    inv = db.query(Invoice).filter(Invoice.id == iid).first()
    if not inv:
        raise ValueError("invoice not found")
    inv.status = "PROCESSED"
    inv.processed_at = datetime.utcnow()
    db.commit()
    db.refresh(inv)
    return inv