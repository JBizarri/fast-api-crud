from fastapi import FastAPI

from .routers import mount_apis

app = FastAPI()
mount_apis(app)
