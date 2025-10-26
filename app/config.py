import os, sys
from dotenv import load_dotenv

load_dotenv()

VALID_ENVS = ["Development", "Production"]
FLASK_ENV = os.getenv("FLASK_ENV")

if FLASK_ENV not in VALID_ENVS:
    sys.exit(f"Invalid FLASK_ENV '{FLASK_ENV}' shoulf be one of {VALID_ENVS}")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


def get_config():
    if FLASK_ENV == "Development"or"Dev":
        return DevelopmentConfig
    elif FLASK_ENV == "Production":
        return ProductionConfig
