from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db, bcrypt
from models.user import User
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)

# Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Username or email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered", "user_id": user.id}), 201


# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))

    return jsonify({"message": "Login successful", "access_token": access_token})


# Get user
@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify({"user_id": user.id, "username": user.username, "email": user.email})


# Update user
@auth_bp.route("/user", methods=["PUT"])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    new_username = data.get("username")
    new_email = data.get("email")
    new_password = data.get("password")

    if new_username:
        user.username = new_username
    if new_email:
        user.email = new_email
    if new_password:
        user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")

    db.session.commit()
    return jsonify({"message": "User updated", "user_id": user.id, "username": user.username, "email": user.email})


# Delete user
@auth_bp.route("/user", methods=["DELETE"])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})
