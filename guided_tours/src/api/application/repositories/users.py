from ..models.account import AccountModel
from ..models.user import UserModel
from ..models import db
from ._repository import _Repository


class UserAlreadyExists(Exception):
    pass


class UsersRepository(_Repository):
    @classmethod
    def add(cls, user):
        """Add account with user to the repo."""
        if UserModel.find_by_username(user["username"]) or UserModel.find_by_email(
            user["email"]
        ):
            raise UserAlreadyExists(
                f"Account for user {user['username']} already exists"
            )

        new_user = UserModel(
            username=user["username"],
            email=user["email"],
            password=UserModel.generate_hash(user["password"]),
        )

        try:
            db.session.add(new_user)
            db.session.flush()

            new_account = AccountModel(user_id=new_user.id)
            db.session.add(new_account)

            db.session.commit()
        except Exception as e:
            # TODO: implement logging
            print(e)
            db.session.rollback()
        else:
            return new_user.id

    @staticmethod
    def get(user):
        """Get a user from the repo."""
        return UserModel.get_by_username_or_password(user)

    @classmethod
    def update(cls, user):
        """Update a user in the repo."""
        cls._add(user)
