import pytest
from app import create_app
from app.extensions import db, jwt_blocklist


@pytest.fixture()
def client():
    jwt_blocklist.clear()
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-only-secret",
    })
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()


def register(client, username="Eva", email="eva@example.com"):
    return client.post("/auth/register", json={
        "username": username, "email": email, "password": "safe-password-123"
    })


def token(client):
    response = client.post("/auth/login", json={
        "username": "Eva", "password": "safe-password-123"
    })
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json['access_token']}"}


def test_register_login_and_duplicate(client):
    assert register(client).status_code == 201
    duplicate = register(client)
    assert duplicate.status_code == 409
    assert "already exists" in duplicate.json["error"]
    assert token(client)
    assert client.post("/auth/login", json={"username": "Eva", "password": "wrong"}).status_code == 401


def test_registration_validation_and_cors(client):
    assert client.post("/auth/register", data="not json").status_code == 400
    assert client.post("/auth/register", json={
        "username": "Eva", "email": "invalid", "password": "123456"
    }).status_code == 400
    response = client.options("/auth/register", headers={
        "Origin": "https://ludo-game-ns8e.vercel.app",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
    })
    assert response.headers["Access-Control-Allow-Origin"] == "https://ludo-game-ns8e.vercel.app"


def test_game_save_resume_and_user_isolation(client):
    register(client)
    headers = token(client)
    created = client.post("/game/new", headers=headers)
    assert created.status_code == 201
    game_id = created.json["game_id"]
    state = {"pieces": [{"id": "red-0", "position": None}], "winner": None}
    assert client.put(f"/game/{game_id}", headers=headers, json={"state": state}).status_code == 200
    resumed = client.get("/game/resume", headers=headers)
    assert resumed.status_code == 200
    assert resumed.json["game_id"] == game_id
    assert resumed.json["state"] == state
    assert register(client, "Other", "other@example.com").status_code == 201
    other = client.post("/auth/login", json={"username": "Other", "password": "safe-password-123"})
    other_headers = {"Authorization": f"Bearer {other.json['access_token']}"}
    assert client.get(f"/game/{game_id}", headers=other_headers).status_code == 404


def test_logout_revokes_token_and_reset_is_honest(client):
    register(client)
    headers = token(client)
    assert client.post("/auth/logout", headers=headers).status_code == 200
    assert client.get("/auth/user", headers=headers).status_code == 401
    reset = client.post("/auth/forgot-password", json={"identifier": "Eva"})
    assert reset.status_code == 501
    assert "not available" in reset.json["error"]
