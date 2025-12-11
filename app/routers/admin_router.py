from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import AdminLoginRequest, LoginResponse
from app.services.admin_auth_service import AdminAuthService

router = APIRouter(prefix="/admin")

@router.post("/login", response_model=LoginResponse)
def login(payload: AdminLoginRequest):
    try:
        token = AdminAuthService.login(payload.email, payload.password)
        return LoginResponse(access_token=token)
    except ValueError:
        raise HTTPException(401, "Invalid credentials")
