from fastapi import FastAPI

from . import auth, companies, users


def include_routers(api: FastAPI):
    api.include_router(auth.endpoint.router)
    api.include_router(companies.endpoint.router)
    api.include_router(users.endpoint.router)
