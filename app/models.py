from datetime import datetime
from app.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # <-- added this
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    players = db.relationship("Player", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default="waiting")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    players = db.relationship("Player", back_populates="game", cascade="all, delete-orphan")
    moves = db.relationship("Move", back_populates="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Game {self.id} - {self.status}>"


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(20))
    position = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))

    user = db.relationship("User", back_populates="players")
    game = db.relationship("Game", back_populates="players")
    moves = db.relationship("Move", back_populates="player", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Player {self.color} - User {self.user_id}>"


class Move(db.Model):
    __tablename__ = "moves"

    id = db.Column(db.Integer, primary_key=True)
    move_number = db.Column(db.Integer, nullable=False)  # <-- added
    description = db.Column(db.String(200))              # <-- added
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))

    player = db.relationship("Player", back_populates="moves")
    game = db.relationship("Game", back_populates="moves")

    def __repr__(self):
        return f"<Move {self.move_number} - {self.description}>"
