from datetime import timedelta
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.extensions import bcrypt, db, jwt_blocklist
from models.user import User

auth_bp = Blueprint("auth", __name__)


def body():
    return request.get_json(silent=True) or {}


def current_user():
    return db.session.get(User, int(get_jwt_identity()))


@auth_bp.post("/register")
def register():
    data = body()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not all(isinstance(value, str) for value in (username, email, password)):
        return jsonify(error="Username, email, and password must be text"), 400
    username, email = username.strip(), email.strip().lower()
    if not username or not email or not password:
        return jsonify(error="Username, email, and password are required"), 400
    if len(password) < 6:
        return jsonify(error="Password must be at least 6 characters"), 400
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        return jsonify(error="Enter a valid email address"), 400
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify(error="Username or email already exists"), 409

    user = User(username=username, email=email,
                password=bcrypt.generate_password_hash(password).decode("utf-8"))
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="Username or email already exists"), 409
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Registration database error")
        return jsonify(error="Registration is temporarily unavailable. Please try again."), 503
    return jsonify(message="User registered", user_id=user.id), 201


@auth_bp.post("/login")
def login():
    data = body()
    username = str(data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username or not password:
        return jsonify(error="Username and password are required"), 400
    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify(error="Invalid username or password"), 401
    token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
    return jsonify(message="Login successful", access_token=token)


@auth_bp.post("/logout")
@jwt_required()
def logout():
    jwt_blocklist.add(get_jwt()["jti"])
    return jsonify(message="Logout successful")


@auth_bp.get("/user")
@jwt_required()
def get_user():
    user = current_user()
    if not user:
        return jsonify(error="User not found"), 404
    return jsonify(user_id=user.id, username=user.username, email=user.email)


@auth_bp.put("/user")
@jwt_required()
def update_user():
    user = current_user()
    if not user:
        return jsonify(error="User not found"), 404
    data = body()
    username = str(data.get("username") or "").strip()
    email = str(data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if username:
        user.username = username
    if email:
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            return jsonify(error="Enter a valid email address"), 400
        user.email = email
    if password:
        if len(password) < 6:
            return jsonify(error="Password must be at least 6 characters"), 400
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="Username or email already exists"), 409
    return jsonify(message="User updated", user_id=user.id,
                   username=user.username, email=user.email)


@auth_bp.delete("/user")
@jwt_required()
def delete_user():
    user = current_user()
    if not user:
        return jsonify(error="User not found"), 404
    db.session.delete(user)
    db.session.commit()
    jwt_blocklist.add(get_jwt()["jti"])
    return jsonify(message="User deleted")


@auth_bp.post("/forgot-password")
def forgot_password():
    # No email provider or reset flow exists yet. Never claim a reset was sent.
    return jsonify(error="Password reset is not available yet. Please contact the project owner."), 501
