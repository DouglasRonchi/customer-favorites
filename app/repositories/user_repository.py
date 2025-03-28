from typing import Optional

from app.models.user import User
from app.utils.conflog import logger
from app.utils.exceptions import UserNotFound


class UserRepository:
    @staticmethod
    def create_user(email: str, name: str, password: str) -> User:
        logger.info("Creating user")
        user = User(email=email, name=name, password=password)
        user.save()
        return user

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        logger.info("Getting user by email")
        user = User.objects(email=email).first()
        if not user:
            return None
        return user
