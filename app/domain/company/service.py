from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from .exceptions import CompanyNotFound, InvalidCompanyName
from .interfaces import CompanyCreate, CompanyUpdate
from .models import Company
from .repository import CompanyRepository


class CompanyService:
    def __init__(self, company_repository: CompanyRepository) -> None:
        self.company_repository = company_repository

    def read_all(self, session: Session) -> List[Company]:
        return self.company_repository.all(session)

    def create(self, session: Session, company_in: CompanyCreate) -> Company:
        if company_in.name.strip() == "":
            raise InvalidCompanyName

        company = Company(**company_in.dict())
        return self.company_repository.create(session, company)

    def read_one(self, session: Session, id: UUID) -> Company:
        if not (company := self.company_repository.one(session, id)):
            raise CompanyNotFound

        return company

    def update(self, session: Session, id: UUID, company_in: CompanyUpdate) -> Company:
        if not self.company_repository.one(session, id):
            raise CompanyNotFound

        if company_in.name.strip() == "":
            raise InvalidCompanyName

        company = Company(**company_in.dict())
        return self.company_repository.replace(session, id, company)

    def delete(self, session: Session, id: UUID) -> None:
        if not self.company_repository.one(session, id):
            raise CompanyNotFound

        self.company_repository.delete(session, id)
