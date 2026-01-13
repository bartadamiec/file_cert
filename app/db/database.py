from pymongo import AsyncMongoClient
from app.core.config import MONGO_PATH

client = AsyncMongoClient(MONGO_PATH)

db = client["file_cert"]

users_collection = db["users"]