from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

from ...domain.auth.service import AuthService
from .containers import Container


class JwtBearer(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=False)

    @inject
    async def __call__(
        self,
        request: Request,
        auth_service: AuthService = Depends(Provide[Container.auth.service]),
    ):
        credentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication scheme."
                )
            if not auth_service.authenticate(credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Token was not provided.")
