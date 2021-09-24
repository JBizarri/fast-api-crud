import enum

import bcrypt
from sqlalchemy import Column, Enum, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from ...database import Base


class AutoName(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class UserStatus(str, AutoName):
    ACTIVE = enum.auto()
    INACTIVE = enum.auto()
    PENDING = enum.auto()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(Integer)
    password = Column(LargeBinary)
    status = Column(Enum(UserStatus), nullable=False)

    company_id = Column(Integer, ForeignKey("company.id"))
    company = relationship("Company", back_populates="users", lazy=False)

    @staticmethod
    def generate_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf8"), self.password)
