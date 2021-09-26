from __future__ import annotations

import json
import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Union
from uuid import UUID

import arrow
import bcrypt
import jwt

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]


class ReservedField(Exception):
    pass


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


@dataclass
class JwtToken:
    token: str

    @classmethod
    def generate_token(
        cls,
        payload: Dict[str, Any],
        expiration: Optional[Union[arrow.Arrow, datetime]] = None,
    ) -> JwtToken:
        if expiration:
            if payload.get("exp"):
                raise ReservedField(
                    "The field 'exp' is reserved for the expiration date."
                )
            payload["exp"] = expiration.timestamp()

        return cls(
            jwt.encode(
                payload, JWT_SECRET, algorithm=JWT_ALGORITHM, json_encoder=UUIDEncoder
            )
        )

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


def generate_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())


def check_password(password: bytes, hased_password: bytes) -> bool:
    return bcrypt.checkpw(password, hased_password)
