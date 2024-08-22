# from pymongo import MongoClient
#
# from config import CONNECTION_STRING_MONGO
# from config import MONGO_DB_NAME
#
# client = MongoClient(CONNECTION_STRING_MONGO)
# db = client[MONGO_DB_NAME]
import sys

from pymongo import MongoClient
from pymongo.errors import  ConfigurationError
from config import CONNECTION_STRING_MONGO, MONGO_DB_NAME
from logger import logger

logger = logger

try:
    # Attempt to create a MongoDB client and connect to the database
    client = MongoClient(CONNECTION_STRING_MONGO)
    db = client[MONGO_DB_NAME]

    # Optionally, check the connection by pinging the server
    client.admin.command('ping')
    logger.info("MongoDB connection established successfully.")

except (ConnectionError, ConfigurationError) as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    sys.exit(1)

except Exception as e:
    logger.error(f"An unexpected error occurred:\n{e}")
    sys.exit(1)

