from ..base_repository import BaseRepository
from .models import Company


class CompanyRepository(BaseRepository[Company]):
    def __init__(self) -> None:
        super().__init__(Company)
