from http import HTTPStatus
from datetime import datetime

from flask_restful import Resource

from ..models.user import UserModel
from ..repositories import UsersRepository, SessionsRepository
from guided_tours_lib.validation.login import UserLoginValidator
from guided_tours_lib.validation.flask import validate


class UserLogin(Resource):
    """Class representing user login resource"""

    _validator = UserLoginValidator

    @validate
    def post(self, data):
        """Post a user's login credentials to verify login."""

        current_user = UsersRepository.get(data)

        if not current_user:
            return {"message": "Not found"}, HTTPStatus.NOT_FOUND

        if not UserModel.verify_hash(data["password"], current_user.password):
            # TODO: only allow user 3 log in attempts then block user for 24 hours and return 403 http status
            # HTTP 404 may also be return here.  In terms of semantics saying the user is
            # "unauthorized" to login seems more correct then to say the user was "not found",
            # however there is a compelling case to be made for returning a 404 in terms of security.
            # This is written into the definition of 404 found here:
            #   "This status code is commonly used when the server does not wish to reveal exactly
            #    why the request has been refused." (W3 HTTP 404 Definition)
            # See: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.5
            return {"message": "Wrong credentials"}, HTTPStatus.UNAUTHORIZED

        if current_user.close_account:
            current_user.close_account = False
            message = "User Account is reopened"
        elif current_user.suspend_account:
            current_user.suspend_account = False
            message = "User Account is un-suspended"
        else:
            message = "Login is successful"

        current_user.last_login = datetime.utcnow()

        UsersRepository.update(current_user)
        SessionsRepository.add(current_user.id)

        return {"message": message, "username": current_user.username}
