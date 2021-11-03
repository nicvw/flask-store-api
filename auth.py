from typing import Optional

from models.user import UserModel


def authenticate(username: str, password: str) -> Optional[UserModel]:
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload) -> Optional[UserModel]:
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
