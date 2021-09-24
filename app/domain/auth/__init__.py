from dependency_injector import containers, providers

from ..user.repository import UserRepository
from .service import AuthService


class AuthContainer(containers.DeclarativeContainer):
    user_repository = providers.Dependency(UserRepository)
    service = providers.Singleton(AuthService, user_repository)
