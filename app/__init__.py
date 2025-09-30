from flask import Flask
from app.db import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    # Config
    app.config.from_object("app.config.Config")

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Import models so Alembic sees them
    from app import models  

    @app.route("/")
    def index():
        return {"message": "Welcome to the Ludo Game Backend!"}

    return app
