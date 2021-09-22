from dependency_injector import containers, providers

from ..company.service import CompanyService
from .repository import UserRepository
from .service import UserService


class UserContainer(containers.DeclarativeContainer):
    company_service = providers.Dependency(CompanyService)

    repository = providers.Singleton(UserRepository)
    service = providers.Singleton(UserService, repository, company_service)
