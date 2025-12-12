from fastapi import APIRouter, Depends
from app.schemas.auth_schema import AdminLoginRequest, LoginResponse
from app.services.admin_auth_service import AdminAuthService

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/login", response_model=LoginResponse)
def login(
    payload: AdminLoginRequest, 
    service: AdminAuthService = Depends()
):
    token = service.login(payload.email, payload.password)
    return LoginResponse(access_token=token)