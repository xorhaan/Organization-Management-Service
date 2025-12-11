from pymongo import MongoClient
from app.config import settings

tenant_client = MongoClient(settings.MONGO_URI)
TENANT_DB_NAME = settings.TENANT_DB
