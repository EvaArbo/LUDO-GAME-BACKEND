import os
from flask import Flask
from app.extensions import init_extensions, db
from routes.auth_routes import auth_bp
from routes.game_routes import game_bp  # import game blueprint

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)

    # Database config: put ludo.db inside instance folder
    instance_path = os.path.join(basedir, "instance")
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'ludo.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    init_extensions(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(game_bp, url_prefix='/game')

    # Import models so create_all() detects them
    with app.app_context():
        from models.user import User
        from models.game import Game
        db.create_all()  # create tables if they don't exist

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
