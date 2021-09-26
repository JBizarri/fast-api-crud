from __future__ import annotations

import enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, Enum, ForeignKey, LargeBinary, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .auth import check_password as _check_password
from ...database import BaseModel
from ..utils import AutoName

if TYPE_CHECKING:
    from ..company.models import Company


class UserStatus(str, AutoName):
    ACTIVE = enum.auto()
    INACTIVE = enum.auto()
    PENDING = enum.auto()


class User(BaseModel):
    email: str = Column(String, unique=True, index=True)
    username: str = Column(String)
    password: bytes = Column(LargeBinary)
    status: UserStatus = Column(Enum(UserStatus), nullable=False)

    company_id: UUID = Column(UUIDType, ForeignKey("company.id"), nullable=False)
    company: Company = relationship("Company", back_populates="users")

    def check_password(self, password: str) -> bool:
        return _check_password(password.encode("utf8"), self.password)
