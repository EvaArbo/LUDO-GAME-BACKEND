from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB   # ✅ import JSONB

class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # ✅ JSONB allows querying JSON fields in Postgres
    state = db.Column(JSONB, nullable=False, default=dict)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Optional helper to return serialized dict
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "state": self.state,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
