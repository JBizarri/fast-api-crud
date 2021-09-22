from typing import List

from sqlalchemy.orm import Session

from .exceptions import CompanyNotFound, InvalidCompanyName
from .interfaces import CompanyCreate, CompanyUpdate
from .models import Company
from .repository import CompanyRepository


class CompanyService:
    def __init__(self, repository: CompanyRepository) -> None:
        self.repository = repository

    def read_all(self, session: Session) -> List[Company]:
        return self.repository.all(session)

    def create(self, session: Session, company_in: CompanyCreate) -> Company:
        company = Company(**company_in.dict())
        return self.repository.create(session, company)

    def read_one(self, session: Session, id: int) -> Company:
        if not (company := self.repository.one(session, id)):
            raise CompanyNotFound(f"Company {id} was not found.")

        return company

    def update(self, session: Session, id: int, company_in: CompanyUpdate) -> Company:
        if not self.repository.one(session, id):
            raise CompanyNotFound(f"Company {id} was not found.")

        if company_in.name.strip() == "":
            raise InvalidCompanyName("Invalid name, please try another.")

        company = Company(**company_in.dict())
        return self.repository.replace(session, id, company)

    def delete(self, session: Session, id: int) -> None:
        if not self.repository.one(session, id):
            raise CompanyNotFound(f"Company {id} was not found.")

        self.repository.delete(session, id)
