import copy
import uuid
from typing import TypeVar
from sqlalchemy.future import select
from typing_extensions import Generic

from Domain.Entities.Base.EntityBase import EntityBase
from Domain.IRepositroies.Base.RepositoryBase import RepositoryBase, T
from Persistence.DatabaseConfig import DatabaseContext
from Persistence.DatabaseConfig.DatabaseContext import AppContext

T = TypeVar("T", bound=EntityBase)

# имплементация базового репозитория проекта
class RepositoryBaseImpl(RepositoryBase, Generic[T]):
    context: DatabaseContext.AppContext
    def __init__(self):
        self.context = AppContext()

    async def add_async(self, entity: T) -> T:
        new_entity: T
        async with self.context.get_async_session().begin() as session:
            session.add(entity)
            await session.commit()
            statement = select(T).where(T.id == entity.id)
            new_entity = await session.get_one(statement)
            await session.close()
        return  new_entity

    async def update_async(self, entity: T) -> T:
        merged_entity: T
        async with self.context.get_async_session().begin() as session:
            q_entity = (select(T)
               .where(T.id == entity.id)
            )
            merged_entity = await session.get_one(q_entity)
            if merged_entity is None:
                await session.close()
                raise ValueError("Сущности с таким ID не существует!")
            merged_entity = copy.deepcopy(entity)
            await session.merge(merged_entity)
            await  session.close()
        return  merged_entity

    async def delete_async(self, entity: T) -> T:
        deleted_entity: T
        async with self.context.get_async_session().begin() as session:
            q_entity = (select(T)
                        .where(T.id == entity.id)
                        )
            deleted_entity = await session.get_one(q_entity)
            if deleted_entity is None:
                await session.close()
                raise ValueError("Сущности с таким ID не существует!")
            await session.delete(deleted_entity)
            await session.close()
        return deleted_entity

    async def get_by_id_async(self, _id: uuid) -> T:
        result: T
        async with self.context.get_async_session() as session:
            q_entity = (select(T)
                        .where(T.id == _id)
                        )
            result = await session.get_one(q_entity)
            await session.close()
        return result

    async def get_all_async(self) -> list[T]:
        entities: list[T]
        async with self.context.get_async_session() as session:
            q = select(T)
            result = await session.execute(q)
            entities = result.scalars().all()
            await  session.close()
        return  entities

    # массовая вставка записей в таблицу
    async def bulk_insert_async(self, entities: list[T]) -> None:
        async with self.context.get_async_session().begin() as session:
            await session.bulk_save_objects(entities)
            await  session.close()

