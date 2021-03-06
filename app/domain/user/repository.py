from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from ..base_repository import BaseRepository
from .models import User, UserStatus


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    def all_with_filters(
        self, session: Session, status: Optional[UserStatus]
    ) -> List[User]:
        query = select(User)
        if status:
            query = query.where(User.status == status)

        return session.execute(query).unique().scalars().all()

    def one_by_email(self, session: Session, email: str) -> User:
        query = select(User).where(User.email == email)
        return session.execute(query).unique().scalar_one_or_none()
