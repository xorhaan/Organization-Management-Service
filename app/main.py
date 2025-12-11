from fastapi import FastAPI
from app.routers.org_router import router as org_router
from app.routers.admin_router import router as admin_router

app = FastAPI(title="Organization Management Service")

app.include_router(org_router)
app.include_router(admin_router)
