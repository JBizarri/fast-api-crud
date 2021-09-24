import sys

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from .containers import Container
from .endpoints import include_routers

container = Container()
container.wire(packages=[sys.modules[__name__]])

v1 = FastAPI()
include_routers(v1)


@v1.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"message": "Invalid fields, please check them and try again."}
        ),
    )


@v1.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"message": exc.detail}),
    )
