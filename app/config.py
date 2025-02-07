import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    DB_URI = os.getenv("DB_URI")
    JWT_KEY = os.getenv("JWT_KEY")
    JWT_EXPIRY_SECS = 3600
