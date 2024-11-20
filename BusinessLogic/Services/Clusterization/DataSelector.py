import datetime, pytz
from Domain.Entities.Comment import Comment
from Domain.Entities.Post import Post
from Domain.Entities.User import User
from Persistence.Repositories.Base.RepositoryBaseImpl import RepositoryBaseImpl
from Persistence.Repositories.UsersRepository import UsersRepository
from Persistence.Repositories.CommentsRepository import CommentsRepository
from Persistence.Repositories.PostsRepository import PostsRepository
from dateutil.relativedelta import relativedelta

utc = pytz.UTC

# сервис выборки данных перед анализом
class DataSelector:
    # репозитории для доступа к данным
    _usersRepository: UsersRepository
    _commentsRepository: CommentsRepository
    _postsRepository: PostsRepository

    # коллекции данных
    users_list: list[User] = []
    comments_list: list[Comment] = []
    posts_list: list[Post] = []

    def __init__(self):
        self._usersRepository = UsersRepository(RepositoryBaseImpl[User]())
        self._postsRepository = PostsRepository(RepositoryBaseImpl[Post]())
        self._commentsRepository = CommentsRepository(RepositoryBaseImpl[Comment]())


    # получение данных из БД
    async def load_data(self):
        self.users_list = await self._usersRepository.repository.get_all_async(User)
        self.comments_list = await self._commentsRepository.repository.get_all_async(Comment)
        self.posts_list = await self._postsRepository.repository.get_all_async(Post)

    # получение возраста и пола каждого пользователя
    def users_age_to_gender(self) -> list:
        result = []
        users_data = [(user.gender, user.birthday) for user in self.users_list]
        for item in users_data:
            date_birth = item[1].replace(tzinfo=utc)
            date_now = datetime.datetime.now().replace(tzinfo=utc)
            rd = relativedelta(date_now, date_birth)
            result.append([item[0], rd.years])
        return result

    # соотношение возраста пользователя с количеством постов
    def users_age_to_number_of_posts(self) -> list:
        result = []
        #user_ids = [user.id for user in self.users_list]
        for user in self.users_list:
            posts_count = sum(1 for p in self.posts_list
                              if p.user_id == user.outer_service_id)
            date_birth = user.birthday.replace(tzinfo=utc)
            date_now = datetime.datetime.now().replace(tzinfo=utc)
            age = relativedelta(date_now, date_birth)
            result.append([age.years, posts_count])
        return result

    # соотношение возраста пользователя с количеством комментариев
    def users_age_to_number_of_comments(self) -> list:
        result = []
        for user in self.users_list:
            comments_count = sum(1 for c in self.comments_list
                              if c.user_id == user.outer_service_id)
            date_birth = user.birthday.replace(tzinfo=utc)
            date_now = datetime.datetime.now().replace(tzinfo=utc)
            age = relativedelta(date_now, date_birth)
            result.append([age.years, comments_count])
        return result
