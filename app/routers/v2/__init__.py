from fastapi import FastAPI
from pydantic import BaseModel

v2 = FastAPI()


class HttpSuccess(BaseModel):
    message: str


@v2.get("/", response_model=HttpSuccess, tags=["root"])
async def root():
    return HttpSuccess(message="Hello World!")
