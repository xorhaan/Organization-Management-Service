from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm 
from app.schemas.auth_schema import LoginResponse
from app.services.admin_auth_service import AdminAuthService

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AdminAuthService = Depends()
):
    token = service.login(form_data.username, form_data.password)
    
    return LoginResponse(access_token=token)