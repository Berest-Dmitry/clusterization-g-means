from typing import List
from pydantic import ValidationError
from BusinessLogic.Services.Common.ModelMapper import ModelMapper
from BusinessLogic.Services.data_extractor_service import DataExtractor
from BusinessLogic.TransportModels.full_user_data_for_clustering import FullUserDataForClustering
from Domain.Entities.Comment import Comment
from Domain.Entities.Post import Post
from Domain.Entities.User import User
from Persistence.Repositories.Base.RepositoryBaseImpl import RepositoryBaseImpl
from Persistence.Repositories.CommentsRepository import CommentsRepository
from Persistence.Repositories.PostsRepository import PostsRepository
from Persistence.Repositories.UsersRepository import UsersRepository


# сервис для загрузки и начальной подготовки данных
class DataDownloader:
    # модели данных
    data_list:  List[FullUserDataForClustering] = []

    # сервисы и репозитории
    _usersRepository: UsersRepository
    _commentsRepository: CommentsRepository
    _postsRepository: PostsRepository
    _dataExtractor: DataExtractor
    _mapper: ModelMapper

    def __init__(self):
        self._usersRepository = UsersRepository(RepositoryBaseImpl[User]())
        self._postsRepository = PostsRepository(RepositoryBaseImpl[Post]())
        self._commentsRepository = CommentsRepository(RepositoryBaseImpl[Comment]())
        self._dataExtractor = DataExtractor()
        self._mapper = ModelMapper()

    # метод загрузки данных из стороннего приложения
    async def extract_data(self):
        #отправляем в сторонний сервис запрос на получение данных и ожидаем данные
        self._dataExtractor.basic_publish()
        self._dataExtractor.basic_consume()
        self.data_list = self._dataExtractor.result_list

        #приступаем к первичной обработке данных
        users_list = []
        comments_list = []
        posts_list = []
        total_users_list = []
        try:
            for data in self.data_list:
                total_users_list.extend(data['FullUserDataForClustering'])

            for data in total_users_list:
                mapped_user = self._mapper.map_to_entity(data, "User")
                users_list.append(mapped_user)

                if isinstance(data["userPosts"], dict):
                    posts_raw = []
                    tmp = data["userPosts"]['post']
                    if isinstance(tmp, list):
                        posts_raw.extend(tmp)
                    elif isinstance(tmp, dict):
                        posts_raw.append(tmp)
                    for post in posts_raw:
                        mapped_post = self._mapper.map_to_entity(post, "Post")
                        posts_list.append(mapped_post)

                if isinstance(data["userComments"], dict):
                    comments_raw = []
                    tmp = data["userComments"]['comment']
                    if isinstance(tmp, list):
                        comments_raw.extend(tmp)
                    elif isinstance(tmp, dict):
                        comments_raw.append(tmp)
                    for comment in comments_raw:
                        mapped_comment = self._mapper.map_to_entity(comment, "Comment")
                        comments_list.append(mapped_comment)
        except (ValidationError, BaseException) as e:
            print(f"Произошла ошибка при обработке полученных данных от стороннего сервиса {str(e)}")

        print("Разбор пользователей закончен, всего перебрано пользователей:" + str(len(users_list)))
        await self.store_data(users_list, posts_list, comments_list)


    # метод сохранения данных в БД
    async def store_data(self, users_list: list[User], posts_list: list[Post], comments_list: list[Comment]):
        await self._usersRepository.bulk_insert_users(users_list)
        await self._postsRepository.bulk_insert_posts(posts_list)
        await self._commentsRepository.bulk_insert_comments(comments_list)

