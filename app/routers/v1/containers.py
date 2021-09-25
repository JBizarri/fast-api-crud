from dependency_injector import containers, providers

from ...domain import company, user


class Container(containers.DeclarativeContainer):
    company = providers.Container(company.CompanyContainer)
    user = providers.Container(user.UserContainer, company_service=company.service)
