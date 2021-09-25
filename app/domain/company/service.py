from typing import List

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
        company = Company(**company_in.dict())
        return self.company_repository.create(session, company)

    def read_one(self, session: Session, id: int) -> Company:
        if not (company := self.company_repository.one(session, id)):
            raise CompanyNotFound(f"Company {id} was not found.")

        return company

    def update(self, session: Session, id: int, company_in: CompanyUpdate) -> Company:
        if not self.company_repository.one(session, id):
            raise CompanyNotFound(f"Company {id} was not found.")

        if company_in.name.strip() == "":
            raise InvalidCompanyName("Invalid name, please try another.")

        company = Company(**company_in.dict())
        return self.company_repository.replace(session, id, company)

    def delete(self, session: Session, id: int) -> None:
        if not self.company_repository.one(session, id):
            raise CompanyNotFound(f"Company {id} was not found.")

        self.company_repository.delete(session, id)
