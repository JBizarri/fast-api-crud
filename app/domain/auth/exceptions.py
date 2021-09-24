from typing import Any, Dict, Optional

from fastapi import status
from fastapi.exceptions import HTTPException


class LoginException(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)
