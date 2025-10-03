# 🎮 Game Backend (Flask + SQLAlchemy + JWT)

This backend provides:
- 🔐 **User Authentication** (signup/login with JWT)
- 🎲 **Game State Management** (save & resume progress)
- 🔗 **REST APIs** for React frontend

Built with **Flask**, **SQLAlchemy**, and **JWT**.

---

## 🛠️ 1. Install Python

Make sure you have **Python 3.8+** installed.

Check version:
```bash
python --version
```

If you see something like `Python 3.10.9`, you’re good.

---

## 📥 2. Clone the Repository

```bash
git clone <repo-url>
cd backend
```

---

## 🐍 3. Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

- **Linux/macOS**
  ```bash
  source venv/bin/activate
  ```

- **Windows (PowerShell)**
  ```bash
  venv\Scripts\activate
  ```

---

## 📦 4. Install Dependencies

Create `requirements.txt` with this content:

```
Flask
Flask-SQLAlchemy
Flask-Migrate
flask-jwt-extended
Werkzeug
Flask-Cors
python-dotenv
psycopg2-binary   # only needed for Postgres
```

Then install:
```bash
pip install -r requirements.txt
```

---

## ⚙️ 5. Environment Variables

Create a file named `.env` in the backend folder:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=super-secret-key
JWT_SECRET_KEY=super-jwt-secret
SQLALCHEMY_DATABASE_URI=sqlite:///app.db   # Dev
# For production: postgresql://user:password@host:5432/dbname
```

---

## 🗄️ 6. Database Setup

Initialize database migrations:
```bash
flask db init
```

Create first migration:
```bash
flask db migrate -m "Initial migration"
```

Apply migration:
```bash
flask db upgrade
```

This will create the `app.db` SQLite file (development DB).

---

## ▶️ 7. Run the Server

```bash
flask run
```

Server will start at:
```
http://127.0.0.1:5000/
```

---

## 🔹 8. Test the API

### Signup
```bash
curl -X POST http://127.0.0.1:5000/auth/signup  -H "Content-Type: application/json"  -d '{"name":"Alice","email":"alice@mail.com","password":"1234"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:5000/auth/login  -H "Content-Type: application/json"  -d '{"email":"alice@mail.com","password":"1234"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "refresh_token": "..."
}
```

Copy the `access_token`.

---

### Create New Game
```bash
curl -X POST http://127.0.0.1:5000/game/new  -H "Content-Type: application/json"  -H "Authorization: Bearer <ACCESS_TOKEN>"  -d '{"token_positions":[0,1,5],"player_turn":1,"dice_value":6}'
```

### Get Game State
```bash
curl -X GET http://127.0.0.1:5000/game/1  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Update Game
```bash
curl -X PUT http://127.0.0.1:5000/game/1  -H "Content-Type: application/json"  -H "Authorization: Bearer <ACCESS_TOKEN>"  -d '{"token_positions":[2,3,7],"player_turn":2,"dice_value":4}'
```

---

## 👥 Team Workflow

- **Adrian** → Flask setup, DB, JWT config  
- **Najma** → Auth API (signup/login)  
- **Maina** → Middleware + route protection  
- **Evah** → Game endpoints (new, get, update)  

---

## 🔐 Security Notes

- Use HTTPS in production
- Keep `SECRET_KEY` and `JWT_SECRET_KEY` private
- Use PostgreSQL for production
- Add refresh tokens + blacklisting if scaling

---

## 📄 License

MIT License.