from typing import Generic

from typing_extensions import TypeVar
from Domain.Entities.Base.EntityBase import EntityBase
from Domain.IRepositroies.Base.RepositoryBase import RepositoryBase

T = TypeVar("T", bound=EntityBase)


class RepositoryMixin:
    repository: RepositoryBase[T]
    def __init__(self, repository: RepositoryBase[T], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = repository