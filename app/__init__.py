from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, migrate, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from models import User, Game
    from routes.auth_routes import auth_bp
    from routes.game_routes import game_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(game_bp, url_prefix="/game")

    return app
