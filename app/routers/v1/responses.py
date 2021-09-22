from typing import Any, Dict, Union

from pydantic import BaseModel


class HttpSuccess(BaseModel):
    message: str


class HttpError(BaseModel):
    message: str


UNPROCESSABLE_ENTITY: Dict[Union[int, str], Dict[str, Any]] = {
    422: {"model": HttpError}
}
