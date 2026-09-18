from fastapi import APIRouter
from app.api.v1 import client_auth, client_home, client_invoice, admin_auth, admin_customer, admin_invoice, admin_dashboard

api_router = APIRouter()
api_router.include_router(client_auth.router, prefix="/client/auth", tags=["A-Auth"])
api_router.include_router(client_home.router, prefix="/client/home", tags=["A-Home"])
api_router.include_router(client_invoice.router, prefix="/client/invoice", tags=["A-Invoice"])
api_router.include_router(admin_auth.router, prefix="/admin/auth", tags=["B-Auth"])
api_router.include_router(admin_customer.router, prefix="/admin/customer", tags=["B-Customer"])
api_router.include_router(admin_invoice.router, prefix="/admin/invoice", tags=["B-Invoice"])
api_router.include_router(admin_dashboard.router, prefix="/admin/dashboard", tags=["B-Dashboard"])