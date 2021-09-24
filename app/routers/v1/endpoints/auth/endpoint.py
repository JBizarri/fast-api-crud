from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from .....database import get_session
from .....domain.auth.service import AuthService
from ...containers import Container
from ...responses import UNPROCESSABLE_ENTITY, HttpError
from .schemas import TokenOutput, UserLoginPost

router = APIRouter(tags=["auth"])


@router.post(
    "/auth",
    response_model=TokenOutput,
    responses={**UNPROCESSABLE_ENTITY, 401: {"model": HttpError}},
)
@inject
async def user_login(
    login_info: UserLoginPost = Body(...),
    session: Session = Depends(get_session),
    auth_service: AuthService = Depends(Provide[Container.auth.service]),
):
    token, token_type = auth_service.login(session, login_info)
    return TokenOutput(token=token, type=token_type)
