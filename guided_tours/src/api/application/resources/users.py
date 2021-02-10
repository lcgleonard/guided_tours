import logging
from http import HTTPStatus

from flask_restful import Resource

from guided_tours_lib.validation.user import UserValidator
from guided_tours_lib.validation.flask import validate

from ..repositories.users import UsersRepository, UserAlreadyExists
from ..repositories.sessions import SessionsRepository
from ..models.user import UserModel


class Users(Resource):
    """User account resource"""

    _validator = UserValidator

    @validate
    def post(self, data):
        """Post new user data and try to register the user by storing the
        data in a persistent database.
        """

        try:
            new_user_id = UsersRepository.add(data)
        except UserAlreadyExists:
            logging.error(f"{data['username']}")
            return {"message": "Registration failed"}, HTTPStatus.BAD_REQUEST
        else:
            SessionsRepository.add(new_user_id)

            return (
                {"message": "User created", "username": data["username"]},
                HTTPStatus.CREATED,
            )

    def put(self, username):
        """Close the user's account.

        Using PUT as this is a major change to the resource:
        the account will be scheduled for deletion.
        """

        current_user = UsersRepository.get({"username": username})

        current_user.close_account = True
        UsersRepository.update(current_user)
        return {"message": "Success"}

    def patch(self, username):
        """Suspend the user's account.

        Using PATCH as this is relatively minor, partial update to the
        resource.
        """
        current_user = UsersRepository.get({"username": username})

        current_user.suspend_account = True
        UsersRepository.update(current_user)
        return {"message": "Success"}

    def delete(self):
        """Delete the user accounts which have been closed for 7 days or more."""
        try:
            UserModel.delete_all_closed_after()
        except Exception as e:
            message = e.message if hasattr(e, "message") else ""
            logging.error(f"Error while deleting user accounts: {message}")
            return (
                {"message": "Failure, check logs"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        else:
            return {"message": "Success"}
