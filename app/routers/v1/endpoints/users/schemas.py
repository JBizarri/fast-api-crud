from pydantic import BaseModel

from .....domain.user.models import UserStatus


class UserPost(BaseModel):
    username: str
    password: str
    email: str
    company_id: int


class UserOutput(BaseModel):
    id: int
    username: str
    email: str
    status: UserStatus
    company_id: int

    class Config:
        orm_mode = True


class UserPut(BaseModel):
    username: str
