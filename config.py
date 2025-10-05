import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.environ['SUPABASE_DB_USER']}:{os.environ['SUPABASE_DB_PASS']}"
        f"@{os.environ['SUPABASE_DB_HOST']}:{os.environ.get('SUPABASE_DB_PORT', 5432)}/"
        f"{os.environ['SUPABASE_DB_NAME']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecret")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-string")
