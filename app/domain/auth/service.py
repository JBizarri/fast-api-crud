import os
from typing import Tuple

import arrow
import jwt
from sqlalchemy.orm import Session

from ..user.repository import UserRepository
from .exceptions import LoginException
from .interfaces import UserLogin


JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def login(self, session: Session, login_info: UserLogin) -> Tuple[str, str]:
        if not (user := self.user_repository.one_by_email(session, login_info.email)):
            raise LoginException("You have entered an invalid email or password")

        if not user.check_password(login_info.password):
            raise LoginException("You have entered an invalid email or password")

        payload = {
            "user_id": user.id,
            "exp": arrow.utcnow().shift(minutes=30).timestamp(),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM), "bearer"

    def authenticate(self, token: str) -> bool:
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except Exception:
            return False
        else:
            return True
