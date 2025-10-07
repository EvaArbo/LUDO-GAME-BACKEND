import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance", "ludo.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "supersecret"  # 🔑 required for JWT sessions
    JWT_SECRET_KEY = "jwt-secret-string"  # 🔑 for flask_jwt_extended
