from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URI)
master_db = client[settings.MASTER_DB]

organizations = master_db["organizations"]
admins = master_db["admins"]
