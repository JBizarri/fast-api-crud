from typing import Generic, List, Optional, Protocol, Type, TypeVar

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

Id = TypeVar("Id")


class StoreClass(Protocol[Id]):
    id: Id


Store = TypeVar("Store", bound=StoreClass)


class BaseRepository(Generic[Store]):
    def __init__(self, store_type: Type[Store]) -> None:
        self._store_type = store_type

    def all(self, session: Session) -> List[Store]:
        query = select(self._store_type)
        return session.execute(query).unique().scalars().all()

    def create(self, session: Session, company: Store) -> Store:
        session.add(company)
        session.commit()
        return company

    def one(self, session: Session, id: Id) -> Optional[Store]:
        query = select(self._store_type).where(self._store_type.id == id)
        return session.execute(query).unique().scalar_one_or_none()

    def replace(self, session: Session, id: Id, company: Store) -> Store:
        company.id = id
        company = session.merge(company)
        session.add(company)
        session.commit()
        return company

    def delete(self, session: Session, id: Id) -> None:
        query = select(self._store_type).where(self._store_type.id == id)
        company = session.execute(query).unique().scalar_one()
        session.delete(company)
        session.commit()
