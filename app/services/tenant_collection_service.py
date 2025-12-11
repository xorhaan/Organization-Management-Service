from app.database.tenant_db import tenant_client, TENANT_DB_NAME

class TenantCollectionService:

    @staticmethod
    def get_tenant_db():
        return tenant_client[TENANT_DB_NAME]

    @staticmethod
    def create_org_collection(org_name: str):
        db = TenantCollectionService.get_tenant_db()
        collection_name = f"org_{org_name.lower()}"

        if collection_name in db.list_collection_names():
            raise ValueError("Collection already exists")

        db.create_collection(collection_name)
        return collection_name
    
    @staticmethod
    def rename_collection(old_name: str, new_name: str):
        db = TenantCollectionService.get_tenant_db()
        old = f"org_{old_name.lower()}"
        new = f"org_{new_name.lower()}"

        if new in db.list_collection_names():
            raise ValueError("New collection name already exists")
        if old not in db.list_collection_names():
            raise ValueError(f"Tenant collection for organization '{old_name}' does not exist.") 
        
        try:
            db[old].rename(new)
        except Exception as e:
            raise ValueError(f"Failed to rename collection: {e}")
    
    @staticmethod
    def delete_collection(org_name: str): 
        db = TenantCollectionService.get_tenant_db()
        collection_name = f"org_{org_name.lower()}"
        db.drop_collection(collection_name)