import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

import arrow
import jwt

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]


class ReservedField(Exception):
    pass


@dataclass
class JwtToken:
    token: str

    @classmethod
    def generate_token(
        cls,
        payload: Dict[str, Any],
        expiration: Optional[Union[arrow.Arrow, datetime]] = None,
    ) -> "JwtToken":
        if expiration:
            if payload.get("exp"):
                raise ReservedField(
                    "The field 'exp' is reserved for the expiration date."
                )
            payload["exp"] = expiration.timestamp()

        return cls(jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM))

    @staticmethod
    def authenticate(token: Union["JwtToken", str]) -> bool:
        token_ = token.token if isinstance(token, JwtToken) else token
        try:
            jwt.decode(token_, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except Exception:
            return False
        else:
            return True

    def __post_init_post_parse__(self):
        self.authenticate(self.token)
