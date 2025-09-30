from flask_sqlalchemy import SQLAlchemy
from app.extensions import db
db = SQLAlchemy()


from .user import User
from .game import Game

__all__ = ["db", "User", "Game"]
