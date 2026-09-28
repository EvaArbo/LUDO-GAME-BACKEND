import os
from datetime import timedelta
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


def database_url():
    url = os.getenv("DATABASE_URL")
    if url:
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://"):]
        if url.startswith("postgresql://"):
            url = "postgresql+psycopg://" + url[len("postgresql://"):]
        return url

    names = ("SUPABASE_DB_HOST", "SUPABASE_DB_NAME", "SUPABASE_DB_USER",
             "SUPABASE_DB_PASS", "SUPABASE_DB_PORT")
    values = {name: os.getenv(name) for name in names}
    if any(values.values()):
        missing = [name for name, value in values.items() if not value]
        if missing:
            raise RuntimeError("Incomplete Supabase database configuration: " + ", ".join(missing))
        return URL.create(
            "postgresql+psycopg",
            username=values["SUPABASE_DB_USER"],
            password=values["SUPABASE_DB_PASS"],
            host=values["SUPABASE_DB_HOST"],
            port=int(values["SUPABASE_DB_PORT"]),
            database=values["SUPABASE_DB_NAME"],
            query={"sslmode": "require"},
        )

    if os.getenv("RENDER") == "true":
        raise RuntimeError("Set DATABASE_URL or the SUPABASE_DB_* environment variables on Render")
    return "sqlite:///ludo-dev.db"


class Config:
    SQLALCHEMY_DATABASE_URI = database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "local-development-only")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "local-jwt-development-only")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
