from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.routers.org_router import router as org_router
from app.routers.admin_router import router as admin_router

app = FastAPI(title="Organization Management Service")

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Catches ValueError (e.g., 'Org already exists') and returns 400 or 404."""
    message = str(exc)
    status_code = status.HTTP_400_BAD_REQUEST
    if "not found" in message.lower():
        status_code = status.HTTP_404_NOT_FOUND
        
    return JSONResponse(
        status_code=status_code,
        content={"detail": message},
    )

@app.exception_handler(PermissionError)
async def permission_error_handler(request: Request, exc: PermissionError):
    """Catches PermissionError and returns 403 Forbidden."""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )

app.include_router(org_router)
app.include_router(admin_router)