from typing import List

from pydantic import BaseModel

from ..users.schemas import UserOutput


class CompanyPost(BaseModel):
    name: str


class CompanyOutput(BaseModel):
    id: int
    name: str

    users: List[UserOutput]

    class Config:
        orm_mode = True


class CompanyPut(BaseModel):
    name: str
