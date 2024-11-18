import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from Domain.Entities.Base.EntityBase import EntityBase
from Persistence.DatabaseConfig import DatabaseContext

T = TypeVar("T", bound=EntityBase)


# базовый репозиторий для работы с БД
class RepositoryBase(ABC, Generic[T]):
    context: DatabaseContext.AppContext

    @abstractmethod
    async def get_all_async(self) -> list[T]:
        """ Метод для получения всех записей таблицы """

    @abstractmethod
    async def add_async(self, entity: T) -> T:
        """ Метод для добавления новой записи """

    @abstractmethod
    async def update_async(self, entity: T) -> T:
        """ Метод для обновления записи """

    @abstractmethod
    async def delete_async(self, entity: T) -> T:
        """ Метод для удаления записи """

    @abstractmethod
    async def get_by_id_async(self, _id: uuid) -> T:
        """ Метод получения записи по ее ID"""

    @abstractmethod
    async def bulk_insert_async(self, entities: list[T]):
        """ Метод множественной вставки записей в таблицу"""

    @abstractmethod
    async def init_context_engine(self) -> bool:
        """метод инициализации контекста БД"""

