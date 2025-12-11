from pydantic import BaseModel

class OrgCreateRequest(BaseModel):
    organization_name: str
    email: str
    password: str

class OrgGetRequest(BaseModel):
    organization_name: str

class OrgUpdateRequest(BaseModel):
    old_name: str
    new_name: str
    email: str
    password: str

class OrgDeleteRequest(BaseModel):
    organization_name: str

class OrgResponse(BaseModel):
    name: str
    collection: str
    admin_email: str
