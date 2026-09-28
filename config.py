import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def database_url():
    url = os.getenv("DATABASE_URL", "sqlite:///ludo-dev.db")
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        url = "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


class Config:
    SQLALCHEMY_DATABASE_URI = database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "local-development-only")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "local-jwt-development-only")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
