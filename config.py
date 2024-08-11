import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

MONGO_DB_NAME = "EasyPack"

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7
RESET_PASSWORD_TIME_EXPIRE = 5

load_dotenv()

JWT_ACCESS_SECRET = os.getenv('JWT_ACCESS_SECRET')
JWT_REFRESH_SECRET = os.getenv('JWT_REFRESH_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
EXCHANGE_RATE_API = os.getenv('EXCHANGE_RATE_API')
CONNECTION_STRING_MONGO = os.getenv('CONNECTION_STRING_MONGO')
reusable_oauth = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/users/login", auto_error=False)

templates_folder = os.path.join('templates')
