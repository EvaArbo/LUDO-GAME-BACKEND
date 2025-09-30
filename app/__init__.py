from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # 🔹 Import models here so Alembic can detect them
    from models import User, Game

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.game_routes import game_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(game_bp, url_prefix="/game")

    return app
