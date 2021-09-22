from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ...database import Base


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    users = relationship(
        "User", back_populates="company", lazy=False, cascade="all, delete"
    )
