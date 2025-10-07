from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from models.game import Game
from datetime import datetime
import json

game_bp = Blueprint("game", __name__)

# Start new or continue existing game
@game_bp.route("/new", methods=["POST"])
@jwt_required()
def new_game():
    user_id = int(get_jwt_identity())
    existing_game = Game.query.filter_by(user_id=user_id).order_by(Game.updated_at.desc()).first()

    if existing_game:
        state = json.loads(existing_game.state)
        if state.get("player_turn") is not None:
            return jsonify({"message": "Continuing existing game", "game_id": existing_game.id, "state": state}), 200

    initial_state = {"token_positions": {}, "player_turn": 1, "dice_value": None}
    game = Game(user_id=user_id, state=json.dumps(initial_state))
    db.session.add(game)
    db.session.commit()

    return jsonify({"message": "New game started", "game_id": game.id, "state": initial_state}), 201


# Get game by ID
@game_bp.route("/<int:game_id>", methods=["GET"])
@jwt_required()
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify({"game_id": game.id, "state": json.loads(game.state)})


# Update game
@game_bp.route("/<int:game_id>", methods=["PUT"])
@jwt_required()
def update_game(game_id):
    game = Game.query.get_or_404(game_id)
    data = request.get_json()
    new_state = data.get("state")

    if not new_state:
        return jsonify({"error": "State is required"}), 400

    game.state = json.dumps(new_state)
    game.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "Game updated", "game_id": game.id, "state": new_state})


# Delete game
@game_bp.route("/<int:game_id>", methods=["DELETE"])
@jwt_required()
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({"message": "Game deleted"})
