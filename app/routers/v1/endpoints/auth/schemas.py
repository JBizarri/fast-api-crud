from pydantic import BaseModel


class UserLoginPost(BaseModel):
    email: str
    password: str


class TokenOutput(BaseModel):
    token: str
    type: str
