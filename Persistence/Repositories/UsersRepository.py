import uuid
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from Domain.Entities.Comment import Comment
from Domain.Entities.Post import Post
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

    # метод подсчета кол-ва строк в таблице
    async def count_rows(self):
        try:
            init_result = await self.repository.init_context_engine()
            total: int
            async with self.repository.context.get_async_session().begin() as session:
                result = await session.execute(
                    select(func.count()).select_from(User)
                )
                total = result.scalar()
                await  session.close()
            return total
        except SQLAlchemyError as e:
            raise e

    # метод получения кол-ва комментариев под постами для каждого пользователя
    async def count_comments_under_posts_for_users(self) -> list:
        try:
            comment_counts_by_posts_and_users = []
            async with self.repository.context.get_async_session().begin() as session:
                result = await session.execute(
                    select(User.id, func.count(Comment.id))
                    .join(Post, Post.user_id == User.outer_service_id)
                    .join(Comment, Comment.post_id == Post.outer_service_id)
                    .group_by(User.id)
                )

                for user_id, comments_count in result:
                    comment_counts_by_posts_and_users.append([user_id, comments_count])
                await session.close()
            return  comment_counts_by_posts_and_users

        except SQLAlchemyError as e:
            raise e

    # метод получения кол-ва ответов на комментарии для каждого пользователя
    async def count_comments_under_comments_for_users(self) -> list:
        try:
            comment_counts_by_comments_and_users = []
            async with self.repository.context.get_async_session().begin() as session:
                parent_comment = aliased(Comment)
                child_comment = aliased(Comment)

                subquery = (
                    select(
                        parent_comment.user_id.label('uid'),
                        parent_comment.id.label('comment_id'),
                        func.count(child_comment.id).label('replies_count')
                    )
                    .select_from(parent_comment)
                    .join(child_comment, parent_comment.id == child_comment.parent_id, isouter=True)  # Соединяем с самой собой
                    .where(parent_comment.parent_id.is_(None))  # Условие для корневых комментариев
                    .group_by(parent_comment.user_id, parent_comment.id)
                    .subquery()
                )

                main_query = (
                    select(
                        subquery.c.uid.label('user_id'),
                        func.sum(subquery.c.replies_count).label('total_replies_count')
                    )
                    .group_by(subquery.c.uid)
                )

                result = await session.execute(main_query)
                for user_id, total_replies_count in result.all():
                    comment_counts_by_comments_and_users.append([user_id, total_replies_count])
                session.close()

            return comment_counts_by_comments_and_users
        except SQLAlchemyError as e:
            raise e

