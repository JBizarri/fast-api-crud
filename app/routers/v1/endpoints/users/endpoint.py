from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .....database import get_session
from .....domain.company.exceptions import CompanyNotFound
from .....domain.user.exceptions import InvalidUsername, UserNotFound
from .....domain.user.service import UserService
from ...containers import Container
from ...responses import UNPROCESSABLE_ENTITY, HttpError, HttpSuccess
from ...security import BearerToken
from .schemas import UserOutput, UserPost, UserPut, UserStatus

router = APIRouter(
    tags=["users"],
    dependencies=[Depends(BearerToken())],
    responses={401: {"model": HttpError}},
)


@router.get("/users", response_model=List[UserOutput], responses=UNPROCESSABLE_ENTITY)
@inject
async def read_users(
    status: Optional[UserStatus] = Query(None),
    session: Session = Depends(get_session),
    user_service: UserService = Depends(Provide[Container.user.service]),
):
    return user_service.read_all(session, status=status)


@router.post(
    "/users",
    response_model=UserOutput,
    responses={
        **UNPROCESSABLE_ENTITY,
        404: {"model": HttpError},
        422: {"model": HttpError},
    },
)
@inject
async def create_user(
    user: UserPost = Body(...),
    session: Session = Depends(get_session),
    user_service: UserService = Depends(Provide[Container.user.service]),
):
    try:
        return user_service.create(session, user)
    except InvalidUsername as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Invalid username, please try another.",
        ) from exc
    except CompanyNotFound as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Company was not found."
        ) from exc


@router.get(
    "/users/{user_id}",
    response_model=UserOutput,
    responses={**UNPROCESSABLE_ENTITY, 404: {"model": HttpError}},
)
@inject
async def read_user(
    user_id: int = Path(...),
    session: Session = Depends(get_session),
    user_service: UserService = Depends(Provide[Container.user.service]),
):
    try:
        return user_service.read_one(session, user_id)
    except UserNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User was not found.") from exc


@router.put(
    "/users/{user_id}",
    response_model=UserOutput,
    responses={**UNPROCESSABLE_ENTITY, 404: {"model": HttpError}},
)
@inject
async def update_user(
    user_id: int = Path(...),
    user: UserPut = Body(...),
    session: Session = Depends(get_session),
    user_service: UserService = Depends(Provide[Container.user.service]),
):
    try:
        return user_service.update(session, user_id, user)
    except InvalidUsername as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Invalid username, please try another.",
        ) from exc
    except UserNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User was not found.") from exc


@router.delete(
    "/users/{user_id}",
    response_model=HttpSuccess,
    responses={**UNPROCESSABLE_ENTITY, 404: {"model": HttpError}},
)
@inject
async def delete_user(
    user_id: int = Path(...),
    session: Session = Depends(get_session),
    user_service: UserService = Depends(Provide[Container.user.service]),
):
    try:
        user_service.delete(session, user_id)
    except UserNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User was not found.") from exc
    else:
        return HttpSuccess(message="OK")
