from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Game, User

game_bp = Blueprint('game', __name__)

# Helper function to get current user from token
def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)

@game_bp.route('/new', methods=['POST'])
@jwt_required()
def create_game():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data or 'state' not in data:
        return jsonify({'error': 'Missing game state'}), 400

    try:
        new_game = Game(user_id=user.id, state=data['state'])
        db.session.add(new_game)
        db.session.commit()
        return jsonify({'message': 'Game created', 'game_id': new_game.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Game creation failed'}), 400

@game_bp.route('/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game(game_id):
    user = get_current_user()
    game = Game.query.filter_by(id=game_id, user_id=user.id).first()

    if not game:
        return jsonify({'error': 'Game not found'}), 404

    return jsonify({'game': game.state}), 200

@game_bp.route('/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data or 'state' not in data:
        return jsonify({'error': 'Missing game state'}), 400

    game = Game.query.filter_by(id=game_id, user_id=user.id).first()
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    try:
        game.state = data['state']
        db.session.commit()
        return jsonify({'message': 'Game updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Game update failed'}), 400
