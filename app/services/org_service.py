from bson import ObjectId
from app.database.master_db import master_db, organizations, admins
from app.utils.hashing import Hash
from app.services.tenant_collection_service import TenantCollectionService

class OrgService:

    @staticmethod
    def create_organization(data):

        name = data.organization_name.lower()

        if organizations.find_one({"name": name}):
            raise ValueError("Organization name already exists")

        collection_name = TenantCollectionService.create_org_collection(name)

        hashed = Hash.hash_password(data.password)
        admin_id = admins.insert_one({
            "email": data.email,
            "password": hashed,
            "org_name": name
        }).inserted_id

        org_id = organizations.insert_one({
            "name": name,
            "collection_name": collection_name,
            "admin_user_id": admin_id
        }).inserted_id

        return {
            "name": name,
            "collection": collection_name,
            "admin_email": data.email
        }

    @staticmethod
    def get_org(name: str):
        org_collection = master_db["organizations"] 

        org = org_collection.find_one({"name": name.lower()}) 

        if not org:
            raise ValueError("Organization not found")

        org["_id"] = str(org["_id"])
        org["admin_user_id"] = str(org["admin_user_id"]) 
        return org

    @staticmethod
    def update_org(old_name: str, new_name: str, email: str, password: str):
        old_name = old_name.lower()
        new_name = new_name.lower()

        if not organizations.find_one({"name": old_name}):
            raise ValueError("Old organization does not exist")

        if organizations.find_one({"name": new_name}):
            raise ValueError("New organization name already exists")

        TenantCollectionService.rename_collection(old_name, new_name)

        hashed = Hash.hash_password(password)
        admins.update_one({"org_name": old_name}, {"$set": {
            "email": email,
            "password": hashed,
            "org_name": new_name
        }})

        organizations.update_one({"name": old_name}, {"$set": {
            "name": new_name,
            "collection_name": f"org_{new_name}"
        }})

        return {"updated": True}

    @staticmethod
    def delete_org(name: str, requesting_admin: str):
        name = name.lower()

        org = organizations.find_one({"name": name})
        if not org:
            raise ValueError("Organization not found")
        clean_admin_id = requesting_admin.strip()
        if org["admin_user_id"] != ObjectId(requesting_admin):
            raise PermissionError("Not authorized to delete this organization")
        TenantCollectionService.delete_collection(name)
        admins.delete_many({"org_name": name})
        organizations.delete_one({"name": name})

        return {"deleted": True}
