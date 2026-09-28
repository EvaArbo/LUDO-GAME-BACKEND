# Ludo Fighters backend

Flask API for accounts and saved game state. The [React frontend](https://github.com/EvaArbo/LUDO-GAME) renders the board and runs the dice, AI turns, and token movement. The backend stores submitted state; it does not validate Ludo rules or provide real-time multiplayer.

## Run locally

Use Python 3.12 or newer and PostgreSQL for deployment. SQLite also works for local development.

```bash
git clone https://github.com/EvaArbo/LUDO-GAME-BACKEND.git
cd LUDO-GAME-BACKEND
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Set unique random `SECRET_KEY` and `JWT_SECRET_KEY` values in your private `.env`. Set `DATABASE_URL` to your database URL if you are using PostgreSQL. Never commit `.env`.

Production start command: `gunicorn wsgi:app`. The app also exposes `app` in `app.py` for existing deployments. Set Render environment variables directly rather than uploading `.env`. Set `FRONTEND_ORIGINS` to a comma-separated list of allowed frontend origins without trailing slashes.

The app currently calls `db.create_all()` on startup for compatibility with earlier deployments. For later schema changes, use Flask-Migrate rather than relying on `create_all()` to alter existing tables.

## Routes

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/auth/register` | Register with `username`, `email`, `password` |
| POST | `/auth/login` | Return one-hour access token for `username` and `password` |
| POST | `/auth/logout` | Revoke token in the current server process |
| GET, PUT, DELETE | `/auth/user` | Manage the signed-in account |
| POST | `/game/new` | Create a saved game |
| GET | `/game/resume` | Return the most recently updated unfinished game |
| GET | `/game/` | List your games |
| GET, PUT, DELETE | `/game/<id>` | Manage one of your games |

Protected routes need `Authorization: Bearer <access_token>`. The `POST /auth/forgot-password` endpoint returns 501 because there is no email delivery or reset flow yet; it does not pretend a reset email was sent.

Example registration:

```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"player1","email":"player1@example.com","password":"example-password"}'
```

## Checks

```bash
pip install pytest
python -m pytest -q
```

The tests cover registration, duplicate accounts, login, CORS preflight, game save and resume, account isolation, logout, and the password reset response.

## Known limits

- Password reset needs a real email provider and a secure reset-token flow.
- The logout blocklist is in memory, so revoked tokens are not shared across workers or retained after a restart. Access tokens expire after one hour.
- The game API stores client-supplied state; it does not enforce dice, capture, turn, or win rules.
