from uuid import UUID

from pydantic import BaseModel


class CompanyPost(BaseModel):
    name: str


class CompanyOutput(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True


class CompanyPut(BaseModel):
    name: str
