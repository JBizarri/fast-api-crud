from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from ...domain.user.auth import JwtToken


class BearerToken(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=False)

    async def __call__(self, request: Request) -> JwtToken:
        credentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication scheme."
                )
            if not JwtToken.authenticate(credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid or expired token.")
            return JwtToken(credentials.credentials)
        else:
            raise HTTPException(status_code=401, detail="Token was not provided.")
