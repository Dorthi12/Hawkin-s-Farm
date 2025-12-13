# db.py
import os
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "hawkins_farm")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI env var is required. Set it in your environment or .env file")

_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=20000)
db = _client[DB_NAME]

def products_collection():
    return db["products"]

def transactions_collection():
    return db["transactions"]

def neighbors_collection():
    return db["item_neighbors"]
