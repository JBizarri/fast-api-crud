from __future__ import annotations

import re
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy_utils import UUIDType

if TYPE_CHECKING:
    Base = object
else:
    Base = declarative_base()


def _camel_case_to_snake_case(string: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class BaseModel(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return _camel_case_to_snake_case(cls.__name__)

    id: UUID = Column(UUIDType, primary_key=True, index=True, default=uuid4)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseModel):
            raise NotImplementedError
        return self.id == other.id
