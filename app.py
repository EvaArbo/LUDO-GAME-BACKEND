import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from app.extensions import db, migrate

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure instance folder exists (so SQLite file can be created)
    instance_path = os.path.join(basedir, "instance")
    os.makedirs(instance_path, exist_ok=True)

    # --------------------------
    # CORS setup for React frontend
    # --------------------------
    CORS(
        app,
        origins=["http://localhost:5173"],  # exact frontend origin
        supports_credentials=True,         # required for Axios withCredentials
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"]
    )

    # --------------------------
    # Initialize DB + migrations
    # --------------------------
    db.init_app(app)
    migrate.init_app(app, db)

    # --------------------------
    # JWT setup
    # --------------------------
    app.config.setdefault("JWT_SECRET_KEY", os.environ.get("JWT_SECRET_KEY", "supersecret"))
    app.config.setdefault("JWT_ACCESS_TOKEN_EXPIRES", None)  # override in Config if needed
    JWTManager(app)

    # --------------------------
    # Register blueprints
    # --------------------------
    from routes.auth_routes import auth_bp
    from routes.game_routes import game_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(game_bp, url_prefix="/game")

    # --------------------------
    # Import models for migrations
    # --------------------------
    with app.app_context():
        from models.user import User
        from models.game import Game
        db.create_all()  # fallback if migrations not run

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
