from fastapi import APIRouter, HTTPException
from app.schemas.org_schema import (
    OrgCreateRequest, OrgGetRequest, OrgUpdateRequest, OrgDeleteRequest, OrgResponse
)
from app.services.org_service import OrgService

router = APIRouter(prefix="/org")

@router.post("/create", response_model=OrgResponse)
def create_org(payload: OrgCreateRequest):
    try:
        return OrgService.create_organization(payload)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/get")
def get_org(organization_name: str):
    try:
        return OrgService.get_org(organization_name)
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.put("/update")
def update_org(payload: OrgUpdateRequest):
    try:
        return OrgService.update_org(
            payload.old_name, payload.new_name, payload.email, payload.password
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/delete")
def delete_org(organization_name: str, admin_id: str):
    try:
        return OrgService.delete_org(organization_name, admin_id)
    except PermissionError as e:
        raise HTTPException(403, str(e))
    except ValueError as e:
        raise HTTPException(404, str(e))
