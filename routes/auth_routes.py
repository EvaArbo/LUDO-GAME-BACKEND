from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

# ✅ Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter((User.username==username)|(User.email==email)).first():
        return jsonify({"error": "Username or email already exists"}), 400

    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered", "user_id": user.id}), 201

# ✅ Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful", "user_id": user.id})

@auth_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    })


@auth_bp.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
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
        user.password = new_password  # later, hash this!

    db.session.commit()

    return jsonify({
        "message": "User updated",
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    })

@auth_bp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"})
