import uuid
from sqlalchemy.exc import SQLAlchemyError
from Domain.Entities.User import User
from Persistence.Repositories.Base.RepositoryBaseImpl import RepositoryBaseImpl
from Persistence.Repositories.Base.RepositoryMixin import RepositoryMixin


class UsersRepository(RepositoryMixin):
    def __init__(self, repository: RepositoryBaseImpl[User]):
        super().__init__(repository)


    # метод добавления нового пользователя
    async def add_user(self, user: User) -> User:
        try:
            added_entity = await self.repository.add_async(user)
            if added_entity is None:
                raise BaseException("Произошла ошибка при сохранении записи о посте")
            return added_entity
        except SQLAlchemyError as e:
            raise

    # метод обновления записи о пользователе
    async def update_user(self, user: User) -> User:
        try:
            updated_entity = await self.repository.update_async(user)
            if updated_entity is None:
                raise BaseException("Произошла ошибка при обновлении записи о посте")
            return updated_entity
        except SQLAlchemyError as e:
            raise

    # метод удаления записи о пользователе
    async def delete_user(self, user: User) -> uuid.UUID:
        try:
            deleted_entity = await  self.repository.delete_async(user)
            if deleted_entity is None:
                raise BaseException("Не удалось выполнить удаление поста")
            return deleted_entity.id
        except SQLAlchemyError as e:
            raise

    # метод получения пользователя по ID
    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        try:
            return await self.repository.get_by_id_async(user_id)
        except SQLAlchemyError as e:
            raise

    # метод получения всех пользователей
    async def get_users(self) -> list[User]:
        try:
            return await self.repository.get_all_async()
        except SQLAlchemyError as e:
            raise

    # метод сохранения списка пользователей
    async def bulk_insert_users(self, users: list[User]) -> None:
        try:
            return  await self.repository.bulk_insert_async(users)
        except SQLAlchemyError as e:
            raise