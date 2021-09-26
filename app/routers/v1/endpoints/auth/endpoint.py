from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..... import get_session
from .....domain.user.exceptions import LoginException
from .....domain.user.service import UserService
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
    user_service: UserService = Depends(Provide[Container.user.service]),
):
    try:
        return user_service.authenticate(session, login_info)
    except LoginException as exc:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "You have entered an invalid email or password.",
        ) from exc
