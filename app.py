# import os
# from flask import Flask
# from app.extensions import init_extensions, db
# from routes.auth_routes import auth_bp
# from routes.game_routes import game_bp  # import game blueprint

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

    # ensure instance folder exists (so sqlite file can be created there)
    instance_path = os.path.join(basedir, "instance")
    os.makedirs(instance_path, exist_ok=True)

    # CORS
    CORS(app)

    # Initialize DB + Migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # JWT setup
    app.config.setdefault("JWT_SECRET_KEY", os.environ.get("JWT_SECRET_KEY", "supersecret"))
    app.config.setdefault("JWT_ACCESS_TOKEN_EXPIRES", None)  # override in Config if needed
    JWTManager(app)

    # Import and register blueprints (explicit)
    # Make sure these module paths match your project structure:
    # routes/auth_routes.py  and  routes/game_routes.py
    from routes.auth_routes import auth_bp
    from routes.game_routes import game_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(game_bp, url_prefix="/game")

    # Import models so they are registered with SQLAlchemy / migrations
    with app.app_context():
        # adjust imports to your models package structure
        from models.user import User
        from models.game import Game
        db.create_all()  # safe fallback if migrations not run

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
