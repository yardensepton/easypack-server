from pymongo import MongoClient
from config import MONGO_PORT, MONGO_DB_NAME

# Provide the connection details
hostname = 'localhost'
port = 27017  # Default MongoDB port

client = MongoClient(hostname, MONGO_PORT)
db = client[MONGO_DB_NAME]
