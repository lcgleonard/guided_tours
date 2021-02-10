from datetime import datetime
from . import db


class AccountModel(db.Model):
    """Models for account of the system."""

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    suspended = db.Column(db.Boolean, unique=False, default=False)
    closed = db.Column(db.Boolean, unique=False, default=False)
    closed_at = db.Column(db.DateTime, unique=False, default=None, nullable=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = db.relationship("UserModel", backref="accounts")
