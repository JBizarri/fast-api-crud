import os

from fastapi import FastAPI

from .database import Base, LocalSessionFactory, connect
from .domain import create_initial_state

SQL_URL = os.environ.get("SQL_URL")
_connection = connect(SQL_URL)
get_session = LocalSessionFactory(_connection)

if os.environ.get("ENV") != "testing":
    create_initial_state(Base, _connection)

from .routers import mount_apis

app = FastAPI()
mount_apis(app)
