from flask_sqlalchemy import SQLAlchemy
from app.extensions import db
db = SQLAlchemy()

# Import models so they register with SQLAlchemy
from .user import User
from .game import Game

__all__ = ["db", "User", "Game"]
