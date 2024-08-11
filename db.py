from pymongo import MongoClient

from config import CONNECTION_STRING_MONGO
from config import MONGO_DB_NAME

client = MongoClient(CONNECTION_STRING_MONGO)
db = client[MONGO_DB_NAME]
