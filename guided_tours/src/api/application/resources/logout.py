from datetime import datetime
from flask_restful import Resource

from guided_tours_lib.validation.logout import UserLogoutValidator
from guided_tours_lib.validation.flask import validate

from ..repositories import UsersRepository, SessionsRepository


class UserLogout(Resource):
    """Resource representing user logout."""

    _validator = UserLogoutValidator

    @validate
    def post(self, data):
        """Updates user session to be logout out"""

        user = UsersRepository.get(data)
        session = SessionsRepository.get(user.id)
        session.last_logout = datetime.utcnow()
        SessionsRepository.update(session)

        return {"message": "Success"}
