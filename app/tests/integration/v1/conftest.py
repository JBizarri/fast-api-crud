import os
import arrow
import pytest
from fastapi.testclient import TestClient

from .... import get_session
from .... import Base, connect, LocalSessionFactory
from ....domain import create_initial_state
from ....domain.user.auth import JwtToken
from ....routers import v1


@pytest.fixture
def v1_client():
    sql_url = os.environ["SQL_URL"]
    connection = connect(sql_url)
    create_initial_state(Base, connection)
    testing_session = LocalSessionFactory(connection)
    v1.dependency_overrides[get_session] = testing_session

    yield TestClient(v1)

    connection.dispose()


@pytest.fixture(scope="module")
def testing_token():
    exp = arrow.utcnow().shift(minutes=5)
    return JwtToken.generate_token({}, expiration=exp).token
