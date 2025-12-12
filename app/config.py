import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MASTER_DB = os.getenv("MASTER_DB", "master_db")
    TENANT_DB = os.getenv("TENANT_DB", "tenant_db")
    JWT_SECRET = os.getenv("JWT_SECRET", "password")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()