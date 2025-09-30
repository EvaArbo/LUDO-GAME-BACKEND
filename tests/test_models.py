from app.models import User, Game, Player, Move
from app.db import db

def test_user_model(app):
    u = User(username="adrian", email="adrian@example.com")
    db.session.add(u)
    db.session.commit()

    assert u.id is not None
    assert u.username == "adrian"

def test_game_and_player(app):
    g = Game(status="ongoing")
    db.session.add(g)
    db.session.commit()

    u = User(username="player1", email="p1@example.com")
    db.session.add(u)
    db.session.commit()

    p = Player(user_id=u.id, game_id=g.id, color="red")
    db.session.add(p)
    db.session.commit()

    assert p.id is not None
    assert p.color == "red"
    assert p.user.username == "player1"
    assert p.game.status == "ongoing"

def test_move(app):
    g = Game(status="ongoing")
    u = User(username="player2", email="p2@example.com")
    db.session.add_all([g, u])
    db.session.commit()

    p = Player(user_id=u.id, game_id=g.id, color="blue")
    db.session.add(p)
    db.session.commit()

    m = Move(player_id=p.id, move_number=1, description="Rolled a 6")
    db.session.add(m)
    db.session.commit()

    assert m.id is not None
    assert "6" in m.description
