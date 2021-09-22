from typing import Any, Dict, Protocol


class CompanyCreate(Protocol):
    name: str

    def dict(self) -> Dict[str, Any]:
        pass


class CompanyUpdate(Protocol):
    name: str

    def dict(self) -> Dict[str, Any]:
        pass
