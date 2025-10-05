from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, migrate, bcrypt, jwt

# In-memory token blocklist
jwt_blocklist = set()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Enable full CORS for your frontend
    CORS(
        app,
        supports_credentials=True,
        origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Content-Type", "Authorization"]
    )

    # ✅ Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # ✅ JWT blocklist handler
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in jwt_blocklist

    # ✅ Import models
    with app.app_context():
        from models.user import User
        from models.game import Game
        db.create_all()  # fallback for dev

    # ✅ Register blueprints
    from routes.auth_routes import auth_bp
    from routes.game_routes import game_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(game_bp, url_prefix="/game")

    @app.route("/")
    def home():
        return {"message": "Flask backend running!"}

    return app
