from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from .....database import get_session
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
    return user_service.authenticate(session, login_info)
