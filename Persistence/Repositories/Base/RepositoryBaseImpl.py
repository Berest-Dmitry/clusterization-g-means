import copy
import uuid
from typing import TypeVar, Type
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from typing_extensions import Generic
from Domain.Entities.Base.EntityBase import EntityBase
from Domain.IRepositroies.Base.RepositoryBase import RepositoryBase, T
from Persistence.DatabaseConfig import DatabaseContext
from Persistence.DatabaseConfig.DatabaseContext import AppContext

T = TypeVar("T", bound=EntityBase)

# Реализация базового репозитория проекта
class RepositoryBaseImpl(RepositoryBase, Generic[T]):
    context: DatabaseContext.AppContext
    def __init__(self):
        # инициализация контекста БД
        self.context = AppContext()

    async def init_context_engine(self) -> bool:
        try:
            if self.context.is_initialized is False:
                await self.context.init_engine()
            return True
        except (SQLAlchemyError, BaseException) as e:
            print(f'Ошибка инициализации контекста БД: {e}')
            return False


    async def add_async(self, entity: T) -> T:
        init_result = await self.init_context_engine()
        new_entity: T
        async with self.context.get_async_session().begin() as session:
            session.add(entity)
            await session.commit()
            statement = select(T).where(T.id == entity.id)
            new_entity = await session.get_one(statement)
            await session.close()
        return  new_entity

    async def update_async(self, entity: T) -> T:
        init_result = await self.init_context_engine()
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
            await session.commit()
            await  session.close()
        return  merged_entity

    async def delete_async(self, entity: T) -> T:
        init_result = await self.init_context_engine()
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
            await session.commit()
            await session.close()
        return deleted_entity

    async def get_by_id_async(self, _id: uuid) -> T:
        init_result = await self.init_context_engine()
        result: T
        async with self.context.get_async_session().begin() as session:
            q_entity = (select(T)
                        .where(T.id == _id)
                        )
            result = await session.get_one(q_entity)
            await session.close()
        return result

    async def get_all_async(self, entity_class: Type[T]) -> list[T]:
        init_result = await self.init_context_engine()
        entities: list[T]
        async with self.context.get_async_session().begin() as session:
            q = select(entity_class)
            result = await session.execute(q)
            entities = result.scalars().all()
            await  session.close()
        return  entities

    # массовая вставка записей в таблицу
    async def bulk_insert_async(self, entities: list[T]) -> None:
        init_result = await self.init_context_engine()
        async with self.context.get_async_session().begin() as session:
            session.add_all(entities)
            await session.commit()
            await  session.close()

