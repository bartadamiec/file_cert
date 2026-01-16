# connection with mongodb
from pymongo import MongoClient
from app.core.config import MONGO_PATH

client = MongoClient(MONGO_PATH)

db = client["file_cert"]

users_collection = db["users"]