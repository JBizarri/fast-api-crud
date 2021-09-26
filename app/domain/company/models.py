from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ...database import BaseModel

if TYPE_CHECKING:
    from ..user.models import User


class Company(BaseModel):
    name: str = Column(String)

    users: List[User] = relationship(
        "User", back_populates="company", cascade="all, delete"
    )
