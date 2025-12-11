import jwt
from datetime import datetime, timedelta, UTC
from app.config import settings

class AuthJWT:
    @staticmethod
    def create_token(admin_id :str, org_id:str, org_name: str):

        expiration_time = datetime.now(UTC) + timedelta(hours = 3)
        payload = {
            "admin_id": admin_id,
            "org_id": org_id,
            "org_name": org_name,
            "exp": expiration_time #cuz datetime.utcnow() is deprecated
        }

        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm = settings.JWT_ALGORITHM
        )

        return token