import os

from fastapi import FastAPI

from .database import Base, LocalSessionFactory, connect
from .domain import create_initial_state

SQL_URL = os.environ.get("SQL_URL")
connection = connect(SQL_URL)
get_session = LocalSessionFactory(connection)


def create_app() -> FastAPI:
    from .routers import mount_apis

    app = FastAPI()
    mount_apis(app)

    create_initial_state(Base, connection)
    return app


app = create_app()
