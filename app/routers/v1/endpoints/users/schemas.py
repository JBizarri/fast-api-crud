from uuid import UUID

from pydantic import BaseModel

from .....domain.user.models import UserStatus


class UserPost(BaseModel):
    username: str
    password: str
    email: str
    company_id: UUID


class UserOutput(BaseModel):
    id: UUID
    username: str
    email: str
    status: UserStatus
    company_id: UUID

    class Config:
        orm_mode = True


class UserPut(BaseModel):
    username: str
