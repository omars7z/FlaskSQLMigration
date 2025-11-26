from datetime import timedelta
import os, sys
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECRET_REFRESH_KEY = os.getenv("SECRET_REFRESH_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    JWT_TOKEN_TIME = timedelta(minutes=int(os.getenv("JWT_TOKEN_TIME")))
    COOKIE_NAME = "access_token"
    COOKIE_HTTP = True
    COOKIE_SECURE = True
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False



def get_config():
    VALID_ENVS = ["Development", "Production"]
    FLASK_ENV = os.getenv("FLASK_ENV")

    if FLASK_ENV not in VALID_ENVS:
        raise ValueError(
            f"Invalid FLASK_ENV '{FLASK_ENV}'. Must be one of {VALID_ENVS}"
        )

    if FLASK_ENV == "Development":
        return DevelopmentConfig
    elif FLASK_ENV == "Production":
        return ProductionConfig
