from bson import ObjectId
from app.database.master_db import organizations, admins, master_db
from app.utils.hashing import Hash
from app.services.tenant_collection_service import TenantCollectionService
from app.config import settings

class OrgService:
    def __init__(self):
        self.tenant_service = TenantCollectionService()

    def create_organization(self, data):
        name = data.organization_name.lower()

        if organizations.find_one({"name": name}):
            raise ValueError("Organization name already exists")
        collection_name = self.tenant_service.create_org_collection(name)

        hashed = Hash.hash_password(data.password)
        admin_id = admins.insert_one({
            "email": data.email,
            "password": hashed,
            "org_name": name
        }).inserted_id

        organizations.insert_one({
            "name": name,
            "collection_name": collection_name,
            "admin_user_id": admin_id,
            "db_connection_uri": settings.MONGO_URI
        })

        return {
            "name": name,
            "collection": collection_name,
            "admin_email": data.email
        }

    def get_org(self, name: str):
        org = organizations.find_one({"name": name.lower()}) 
        if not org:
            raise ValueError("Organization not found")
        
        org["_id"] = str(org["_id"])
        org["admin_user_id"] = str(org["admin_user_id"]) 
        is_local = "localhost" in settings.MONGO_URI or "127.0.0.1" in settings.MONGO_URI
        if not is_local:
            if "db_connection_uri" in org:
                del org["db_connection_uri"]
        return org

    def update_org(self, new_name: str, email: str, password: str):
        admin = admins.find_one({"email": email})
        if not admin:
            raise ValueError("Invalid credentials") 
        if not Hash.verify(password, admin["password"]):
            raise ValueError("Invalid credentials")

        old_name = admin["org_name"]
        
        old_name_lower = old_name.lower()
        new_name_lower = new_name.lower()

        if old_name_lower == new_name_lower:
            return {"updated": False, "message": "New name is same as old name"}

        if organizations.find_one({"name": new_name_lower}):
            raise ValueError("New organization name already exists")
        self.tenant_service.rename_collection(old_name_lower, new_name_lower)

        organizations.update_one(
            {"name": old_name_lower}, 
            {"$set": {
                "name": new_name_lower,
                "collection_name": f"org_{new_name_lower}"
            }}
        )
        
        admins.update_one(
            {"email": email},
            {"$set": {"org_name": new_name_lower}}
        )

        return {
            "updated": True, 
            "old_name": old_name_lower, 
            "new_name": new_name_lower
        }

    def delete_org(self, name: str, requesting_admin_id: str):
        name = name.lower()
        org = organizations.find_one({"name": name})
        
        if not org:
            raise ValueError("Organization not found")
            
        if str(org["admin_user_id"]) != requesting_admin_id:
            raise PermissionError("Not authorized to delete this organization")

        self.tenant_service.delete_collection(name)
        admins.delete_many({"org_name": name})
        organizations.delete_one({"name": name})

        return {"deleted": True}