import os
from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, migrate, bcrypt, jwt, jwt_blocklist


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    origins = [origin.strip() for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "https://ludo-game-ns8e.vercel.app,http://localhost:5173,http://127.0.0.1:5173",
    ).split(",") if origin.strip()]
    CORS(app, origins=origins, supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in jwt_blocklist

    from models.user import User  # noqa: F401
    from models.game import Game  # noqa: F401
    from routes.auth_routes import auth_bp
    from routes.game_routes import game_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(game_bp, url_prefix="/game")

    @app.get("/")
    def home():
        return {"message": "Ludo backend running"}

    # Existing deployments created tables on startup. Keep that behavior until
    # all deployments are migrated, while exposing Flask-Migrate for upgrades.
    with app.app_context():
        db.create_all()

    return app
