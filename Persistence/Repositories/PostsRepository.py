import uuid
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from Domain.Entities.Post import Post
from Persistence.Repositories.Base.RepositoryBaseImpl import RepositoryBaseImpl
from Persistence.Repositories.Base.RepositoryMixin import RepositoryMixin


#репозиторий работы с постами пользователей
class PostsRepository(RepositoryMixin):
    def __init__(self, repository: RepositoryBaseImpl[Post]):
        super().__init__(repository)

    # метод добавления нового поста
    async def add_post(self, post: Post) -> Post:
        try:
            added_entity = await self.repository.add_async(post)
            if added_entity is None:
                raise BaseException("Произошла ошибка при сохранении записи о посте")
            return added_entity
        except SQLAlchemyError as e:
            raise

    # метод обновления поста
    async def update_post(self, post: Post) -> Post:
        try:
            updated_entity = await self.repository.update_async(post)
            if updated_entity is None:
                raise BaseException("Произошла ошибка при обновлении записи о посте")
            return updated_entity
        except SQLAlchemyError as e:
            raise

    # метод удаления записи о посте
    async def delete_post(self, post: Post) -> uuid.UUID:
        try:
            deleted_entity = await  self.repository.delete_async(post)
            if deleted_entity is None:
                raise BaseException("Не удалось выполнить удаление поста")
            return deleted_entity.id
        except SQLAlchemyError as e:
            raise

    # метод получения списка всех постов выбранного пользователя
    async def get_posts_of_user(self, user_id: uuid.UUID) -> list[Post]:
        try:
            result: list[Post]
            async with self.repository.context.get_async_session().begin() as session:
                posts_query = select(Post).where(Post.user_id == user_id)
                result = await  session.execute(posts_query)
                await session.close()
            return  result
        except SQLAlchemyError as e:
            raise

