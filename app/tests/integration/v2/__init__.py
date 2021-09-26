from fastapi.testclient import TestClient

from ....routers import v2

v2_client = TestClient(v2)
