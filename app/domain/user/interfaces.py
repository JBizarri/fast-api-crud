from typing import Any, Dict, Protocol
from uuid import UUID


class UserCreate(Protocol):
    username: str
    password: str
    email: str
    company_id: UUID

    def dict(self) -> Dict[str, Any]:
        pass


class UserUpdate(Protocol):
    username: str

    def dict(self) -> Dict[str, Any]:
        pass


class UserLogin(Protocol):
    email: str
    password: str
