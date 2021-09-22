from fastapi.applications import FastAPI

from .v1 import v1
from .v2 import v2


def mount_apis(app: FastAPI):
    app.mount("/api/v1", v1)
    app.mount("/api/v2", v2)
