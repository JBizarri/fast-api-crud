from typing import Protocol


class UserLogin(Protocol):
    email: str
    password: str
