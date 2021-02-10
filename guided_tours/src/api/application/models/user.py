from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from . import db


class UserModel(db.Model):
    """Models for users of the system."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    account = db.relationship("AccountModel", uselist=False, backref="users")  # 1 to 1
    session = db.relationship(
        "SessionModel", backref="users"
    )  # 1 to many (no uselist=False)

    @property
    def suspend_account(self) -> bool:
        """Suspend the user's account"""
        return self.account.suspended

    @suspend_account.setter
    def suspend_account(self, value: bool) -> None:
        """Set the the user's account as suspended"""
        self.account.suspended = value

    @property
    def close_account(self) -> bool:
        """Close the user's account"""
        return self.account.closed

    @close_account.setter
    def close_account(self, value: bool) -> None:
        """Set the the user's account as closed"""
        self.account.closed = value

        self.account.closed_at = datetime.utcnow() if value is True else None

    @classmethod
    def get_by_username_or_password(cls, data):
        """Get the current user based on username or email supplied"""
        if "username" in data:
            current_user = cls.find_by_username(data["username"])
        else:
            current_user = cls.find_by_email(data["email"])

        return current_user

    @classmethod
    def find_by_username(cls, username):
        """Find user by their username."""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str):
        """Find user by their email."""
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def generate_hash(password: str) -> str:
        """Generate's sha256 hash of user's password with salt."""
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hashed_password: str) -> bool:
        """Verify the submitted password against the encrypted password."""
        return pbkdf2_sha256.verify(password, hashed_password)

    @classmethod
    def delete_all_closed_after(cls, time_range=None):
        """Delete all user account's which are closed after a given time range."""
        if time_range is None:
            # Defaulting to one week ago
            time_range = datetime.now() - timedelta(days=7)

        # synchronize_session="fetch" - "performs a select query before the delete
        # to find objects that are matched by the delete query and need to be
        # removed from the session. Matched objects are removed from the session."
        # See: https://kite.com/python/docs/sqlalchemy.orm.query.Query.delete
        return cls.query.filter(
            db.and_(cls.account.last_login <= time_range), cls.account.closed
        ).delete(synchronize_session="fetch")
