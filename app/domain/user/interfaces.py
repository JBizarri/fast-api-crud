from typing import Any, Dict, Protocol


class UserCreate(Protocol):
    username: str
    password: str
    email: str
    company_id: int

    def dict(self) -> Dict[str, Any]:
        pass


class UserUpdate(Protocol):
    username: str

    def dict(self) -> Dict[str, Any]:
        pass
