from ..models.session import SessionModel
from ._repository import _Repository


class SessionsRepository(_Repository):
    @classmethod
    def add(cls, user_id):
        """Add user session to the repo."""

        new_session = SessionModel(user_id=user_id)
        return cls._add(new_session)

    @classmethod
    def get(cls, user_id):
        """Get the user's current/last session"""
        return SessionModel.find_last_session(user_id)

    @classmethod
    def update(cls, session):
        """Update an existing session."""
        cls._add(session)
