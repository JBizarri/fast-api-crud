from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .....database import get_session
from .....domain.company.exceptions import CompanyNotFound, InvalidCompanyName
from .....domain.company.service import CompanyService
from ...containers import Container
from ...responses import UNPROCESSABLE_ENTITY, HttpError, HttpSuccess
from ...security import BearerToken
from .schemas import CompanyOutput, CompanyPost, CompanyPut

router = APIRouter(
    tags=["companies"],
    dependencies=[Depends(BearerToken())],
    responses={401: {"model": HttpError}},
)


@router.get("/companies", response_model=List[CompanyOutput])
@inject
async def read_companies(
    session: Session = Depends(get_session),
    company_service: CompanyService = Depends(Provide[Container.company.service]),
):
    return company_service.read_all(session)


@router.post("/companies", response_model=CompanyOutput, responses=UNPROCESSABLE_ENTITY)
@inject
async def create_company(
    company: CompanyPost = Body(...),
    session: Session = Depends(get_session),
    company_service: CompanyService = Depends(Provide[Container.company.service]),
):
    try:
        return company_service.create(session, company)
    except InvalidCompanyName as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid name, please try another."
        ) from exc


@router.get(
    "/companies/{company_id}",
    response_model=CompanyOutput,
    responses={**UNPROCESSABLE_ENTITY, 404: {"model": HttpError}},
)
@inject
async def read_company(
    company_id: int = Path(...),
    session: Session = Depends(get_session),
    company_service: CompanyService = Depends(Provide[Container.company.service]),
):
    try:
        return company_service.read_one(session, company_id)
    except CompanyNotFound as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Company was not found."
        ) from exc


@router.put(
    "/companies/{company_id}",
    response_model=CompanyOutput,
    responses={**UNPROCESSABLE_ENTITY, 404: {"model": HttpError}},
)
@inject
async def update_company(
    company_id: int = Path(...),
    company: CompanyPut = Body(...),
    session: Session = Depends(get_session),
    company_service: CompanyService = Depends(Provide[Container.company.service]),
):
    try:
        return company_service.update(session, company_id, company)
    except CompanyNotFound as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Company was not found."
        ) from exc
    except InvalidCompanyName as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid name, please try another."
        ) from exc


@router.delete(
    "/companies/{company_id}",
    response_model=HttpSuccess,
    responses={**UNPROCESSABLE_ENTITY, 404: {"model": HttpError}},
)
@inject
async def delete_company(
    company_id: int = Path(...),
    session: Session = Depends(get_session),
    company_service: CompanyService = Depends(Provide[Container.company.service]),
):
    try:
        company_service.delete(session, company_id)
    except CompanyNotFound as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Company was not found."
        ) from exc
    else:
        return HttpSuccess(message="OK")
