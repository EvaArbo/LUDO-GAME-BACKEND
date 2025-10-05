from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"  # ✅ must match Game.user_id foreign key

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship to Game
    games = db.relationship("Game", backref="user", lazy=True, cascade="all, delete-orphan")
