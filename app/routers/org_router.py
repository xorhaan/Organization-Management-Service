from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.org_schema import (
    OrgCreateRequest, OrgUpdateRequest, OrgResponse
)
from app.services.org_service import OrgService
from app.dependencies import get_current_admin

router = APIRouter(prefix="/org", tags=["Organization"])

@router.post("/create", response_model=OrgResponse, status_code=status.HTTP_201_CREATED)
def create_org(
    payload: OrgCreateRequest, 
    service: OrgService = Depends()
):
    return service.create_organization(payload)

@router.get("/get")
def get_org(
    organization_name: str, 
    service: OrgService = Depends()
):
    return service.get_org(organization_name)

@router.put("/update")
def update_org(
    payload: OrgUpdateRequest, 
    service: OrgService = Depends()
):
    return service.update_org(
        new_name=payload.organization_name,
        email=payload.email,
        password=payload.password
    )

@router.delete("/delete")
def delete_org(
    organization_name: str, 
    current_admin: dict = Depends(get_current_admin), 
    service: OrgService = Depends()
):
    requesting_admin_id = current_admin["admin_id"]
    
    return service.delete_org(organization_name, requesting_admin_id)