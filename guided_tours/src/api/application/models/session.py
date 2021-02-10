from datetime import datetime
from sqlalchemy import desc
from . import db


class SessionModel(db.Model):
    """Models for user sessions."""

    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    last_login = db.Column(
        db.DateTime, unique=False, default=datetime.utcnow(), nullable=True
    )
    last_logout = db.Column(db.DateTime, unique=False, default=None, nullable=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = db.relationship("UserModel", backref="sessions")

    @classmethod
    def find_last_session(cls, user_id):
        """Find last user session by their user id."""
        return (
            cls.query.filter_by(user_id=user_id).order_by(desc(cls.last_login)).first()
        )
