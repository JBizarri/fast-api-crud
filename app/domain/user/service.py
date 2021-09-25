from typing import List, Optional

import arrow
from sqlalchemy.orm import Session

from ..company.exceptions import CompanyNotFound
from ..company.service import CompanyService
from .auth import JwtToken
from .exceptions import InvalidUsername, LoginException, UserNotFound
from .interfaces import UserCreate, UserLogin, UserUpdate
from .models import User, UserStatus
from .repository import UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        company_service: CompanyService,
    ) -> None:
        self.user_repository = user_repository
        self.company_service = company_service

    def read_all(
        self, session: Session, status: Optional[UserStatus] = None
    ) -> List[User]:
        return self.user_repository.all_with_filters(session, status=status)

    def create(self, session: Session, user_in: UserCreate) -> User:
        if not self.company_service.read_one(session, user_in.company_id):
            raise CompanyNotFound(f"Company {user_in.company_id} was not found")

        user_dict = user_in.dict()
        hashed_password = User.generate_password(user_dict.pop("password"))
        user_dict["password"] = hashed_password

        user = User(**user_dict, status=UserStatus.PENDING)
        return self.user_repository.create(session, user)

    def read_one(self, session: Session, id: int) -> User:
        if not (user := self.user_repository.one(session, id)):
            raise UserNotFound(f"User {id} was not found.")

        return user

    def update(self, session: Session, id: int, user_in: UserUpdate) -> User:
        if not self.user_repository.one(session, id):
            raise UserNotFound(f"User {id} was not found.")

        if user_in.username == "admin":
            raise InvalidUsername("Invalid username, please try another.")

        if user_in.username.strip() == "":
            raise InvalidUsername("Username can't be empty, please try another.")

        user = User(**user_in.dict())
        return self.user_repository.replace(session, id, user)

    def delete(self, session: Session, id: int) -> None:
        if not self.user_repository.one(session, id):
            raise UserNotFound(f"User {id} was not found.")

        self.user_repository.delete(session, id)

    def authenticate(self, session: Session, login_info: UserLogin) -> JwtToken:
        if not (user := self.user_repository.one_by_email(session, login_info.email)):
            raise LoginException("You have entered an invalid email or password")

        if not user.check_password(login_info.password):
            raise LoginException("You have entered an invalid email or password")

        payload = {"user_id": user.id}
        expiration = arrow.utcnow().shift(minutes=30)
        return JwtToken.generate_token(payload, expiration=expiration)
