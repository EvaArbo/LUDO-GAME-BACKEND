from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from models.game import Game
from datetime import datetime
from sqlalchemy import func

game_bp = Blueprint("game", __name__)

def handle_options():
    return '', 200


# --------------------------
# Start new game
# --------------------------
@game_bp.route("/new", methods=["POST", "OPTIONS"])
@jwt_required()
def start_new_game():
    if request.method == "OPTIONS":
        return handle_options()

    user_id = int(get_jwt_identity())

    # Always start a fresh game (don’t reuse unfinished)
    initial_state = {
        "pieces": [],
        "scores": {"Red": 0, "Green": 0, "Yellow": 0, "Blue": 0},
        "currentPlayer": "Red",
        "diceValue": None,
        "winner": None
    }

    game = Game(user_id=user_id, state=initial_state)
    db.session.add(game)
    db.session.commit()

    return jsonify({
        "message": "New game started",
        "game_id": game.id,
        "state": initial_state,
        "updated_at": game.updated_at.isoformat()
    }), 201


# --------------------------
# Resume last unfinished game
# --------------------------
@game_bp.route("/resume", methods=["GET", "OPTIONS"])
@jwt_required()
def resume_game():
    if request.method == "OPTIONS":
        return handle_options()

    user_id = int(get_jwt_identity())

    # Find latest unfinished game where winner is null
    game = (
        Game.query
        .filter(Game.user_id == user_id, Game.state['winner'].astext.is_(None))
        .order_by(Game.updated_at.desc())
        .first()
    )

    if not game:
        return jsonify({"message": "No unfinished game found"}), 404

    return jsonify({
        "message": "Resumed game",
        "game_id": game.id,
        "state": game.state,
        "updated_at": game.updated_at.isoformat()
    }), 200


# --------------------------
# List all games for user
# --------------------------
@game_bp.route("/", methods=["GET", "OPTIONS"])
@jwt_required()
def list_games():
    if request.method == "OPTIONS":
        return handle_options()

    user_id = int(get_jwt_identity())
    games = Game.query.filter_by(user_id=user_id).order_by(Game.updated_at.desc()).all()

    return jsonify([
        {
            "game_id": g.id,
            "state": g.state,
            "created_at": g.created_at.isoformat(),
            "updated_at": g.updated_at.isoformat()
        } for g in games
    ]), 200


# --------------------------
# Get game by ID
# --------------------------
@game_bp.route("/<int:game_id>", methods=["GET", "OPTIONS"])
@jwt_required()
def get_game(game_id):
    if request.method == "OPTIONS":
        return handle_options()

    user_id = int(get_jwt_identity())
    game = Game.query.filter_by(id=game_id, user_id=user_id).first()
    if not game:
        return jsonify({"error": "Game not found"}), 404

    return jsonify({
        "game_id": game.id,
        "state": game.state,
        "updated_at": game.updated_at.isoformat()
    }), 200


# --------------------------
# Update game state
# --------------------------
@game_bp.route("/<int:game_id>", methods=["PUT", "OPTIONS"])
@jwt_required()
def update_game(game_id):
    if request.method == "OPTIONS":
        return handle_options()

    user_id = int(get_jwt_identity())
    game = Game.query.filter_by(id=game_id, user_id=user_id).first()
    if not game:
        return jsonify({"error": "Game not found"}), 404

    data = request.get_json()
    new_state = data.get("state")
    if not new_state:
        return jsonify({"error": "State is required"}), 400

    game.state = new_state
    db.session.commit()

    return jsonify({
        "message": "Game updated",
        "game_id": game.id,
        "state": new_state,
        "updated_at": game.updated_at.isoformat()
    }), 200


# --------------------------
# Delete game
# --------------------------
@game_bp.route("/<int:game_id>", methods=["DELETE", "OPTIONS"])
@jwt_required()
def delete_game(game_id):
    if request.method == "OPTIONS":
        return handle_options()

    user_id = int(get_jwt_identity())
    game = Game.query.filter_by(id=game_id, user_id=user_id).first()
    if not game:
        return jsonify({"error": "Game not found"}), 404

    db.session.delete(game)
    db.session.commit()
    return jsonify({"message": "Game deleted"}), 200
