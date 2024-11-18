import uuid
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from Domain.Entities.Comment import Comment
from Persistence.Repositories.Base.RepositoryBaseImpl import RepositoryBaseImpl
from Persistence.Repositories.Base.RepositoryMixin import RepositoryMixin


class CommentsRepository(RepositoryMixin):
    def __init__(self, repository: RepositoryBaseImpl[Comment]):
        super().__init__(repository)

        # метод добавления нового пользователя
    async def add_comment(self, comment: Comment) -> Comment:
        try:
            added_entity = await self.repository.add_async(comment)
            if added_entity is None:
                raise BaseException("Произошла ошибка при сохранении записи о посте")
            return added_entity
        except SQLAlchemyError as e:
            raise

    # метод обновления записи о пользователе
    async def update_comment(self, comment: Comment) -> Comment:
        try:
            updated_entity = await self.repository.update_async(comment)
            if updated_entity is None:
                raise BaseException("Произошла ошибка при обновлении записи о посте")
            return updated_entity
        except SQLAlchemyError as e:
            raise

    # метод удаления записи о пользователе
    async def delete_comment(self, comment: Comment) -> uuid.UUID:
        try:
            deleted_entity = await  self.repository.delete_async(comment)
            if deleted_entity is None:
                raise BaseException("Не удалось выполнить удаление поста")
            return deleted_entity.id
        except SQLAlchemyError as e:
            raise

    # метод получения списка комментариев данного пользователя
    async def get_comments_of_user(self, user_id: uuid.UUID) -> list[Comment]:
        try:
            result: list[Comment]
            async with self.repository.context.get_async_session().begin() as session:
                comments_query = select(Comment).where(Comment.user_id == user_id)
                result = await session.execute(comments_query)
            return  result
        except SQLAlchemyError as e:
            raise

    # метод сохранения списка пользователей
    async def bulk_insert_comments(self, comments: list[Comment]) -> None:
        try:
            return await self.repository.bulk_insert_async(comments)
        except SQLAlchemyError as e:
            raise

    # метод подсчета кол-ва строк в таблице
    async def count_rows(self):
        try:
            init_result = await self.repository.init_context_engine()
            total: int
            async with self.repository.context.get_async_session().begin() as session:
                result = await session.execute(
                    select(func.count()).select_from(Comment)
                )
                total = result.scalar()
                await  session.close()
            return total
        except SQLAlchemyError as e:
            raise e
