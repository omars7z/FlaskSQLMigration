from datetime import timedelta
import os, sys
from dotenv import load_dotenv

load_dotenv()

VALID_ENVS = ["Development", "Production"]
FLASK_ENV = os.getenv("FLASK_ENV")

if FLASK_ENV not in VALID_ENVS:
    sys.exit(f"Invalid FLASK_ENV '{FLASK_ENV}' shoulf be one of {VALID_ENVS}")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECRET_REFRESH_KEY = os.getenv("SECRET_REFRESH_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    JWT_TOKEN_TIME = timedelta(hours=int(os.getenv("JWT_TOKEN_TIME", 1)))
    COOKIE_NAME = "access_token"
    COOKIE_HTTP = True
    COOKIE_SECURE = True

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False


def get_config():
    if FLASK_ENV == "Development"or"Dev":
        return DevelopmentConfig
    elif FLASK_ENV == "Production"or"Config":
        return ProductionConfig
