from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


def connect(url: Optional[str] = None) -> Engine:
    url = url or "sqlite://"
    connect_args = {}
    if url.startswith("sqlite://"):
        connect_args["check_same_thread"] = False

    return create_engine(url, connect_args=connect_args)


class LocalSessionFactory:
    def __init__(self, engine: Engine):
        self._engine = engine

    def __call__(self) -> Generator:
        LocalSession = sessionmaker(autocommit=False, bind=self._engine)
        session = LocalSession()
        try:
            yield session
        finally:
            session.close()
