from dependency_injector import containers, providers

from .repository import CompanyRepository
from .service import CompanyService


class CompanyContainer(containers.DeclarativeContainer):
    repository = providers.Singleton(CompanyRepository)
    service = providers.Singleton(CompanyService, repository=repository)
