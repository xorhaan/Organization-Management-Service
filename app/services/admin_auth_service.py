from app.database.master_db import admins, organizations
from app.utils.hashing import Hash
from app.utils.auth import AuthJWT

class AdminAuthService:

    @staticmethod
    def login(email: str, password: str):
        admin = admins.find_one({"email": email})
        if not admin:
            raise ValueError("Invalid credentials")

        if not Hash.verify(password, admin["password"]):
            raise ValueError("Invalid credentials")

        org = organizations.find_one({"name": admin["org_name"]})
        token = AuthJWT.create_token(
            str(admin["_id"]),
            str(org["_id"]),
            org["name"]
        )

        return token
