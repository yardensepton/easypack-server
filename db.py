from pymongo import MongoClient
from config import MONGO_DB_NAME

# Provide the connection details
connection_string = 'mongodb+srv://yardensepton:yardensepton@cluster.oxojwyy.mongodb.net/'
client = MongoClient(connection_string)
db = client[MONGO_DB_NAME]