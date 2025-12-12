from app.database.tenant_db import tenant_client, TENANT_DB_NAME

class TenantCollectionService:
    def get_tenant_db(self):
        return tenant_client[TENANT_DB_NAME]

    def create_org_collection(self, org_name: str):
        db = self.get_tenant_db()
        collection_name = f"org_{org_name.lower()}"

        if collection_name in db.list_collection_names():
            pass 
        else:
            db.create_collection(collection_name)
            
        return collection_name
    
    def rename_collection(self, old_name: str, new_name: str):
        db = self.get_tenant_db()
        old = f"org_{old_name.lower()}"
        new = f"org_{new_name.lower()}"

        if new in db.list_collection_names():
            raise ValueError("New collection name already exists")
        if old not in db.list_collection_names():
            raise ValueError(f"Tenant collection '{old}' does not exist.") 
        
        db[old].rename(new)
    
    def delete_collection(self, org_name: str): 
        db = self.get_tenant_db()
        collection_name = f"org_{org_name.lower()}"
        db.drop_collection(collection_name)