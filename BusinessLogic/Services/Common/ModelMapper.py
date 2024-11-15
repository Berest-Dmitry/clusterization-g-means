from datetime import datetime
from Domain.Entities.Base.EntityBase import EntityBase
from Domain.Entities.Comment import Comment
from Domain.Entities.Post import Post
from Domain.Entities.User import User


# сервис маппинга сущностей и моделей
class ModelMapper:

    #базовый метод маппера (в сущность)
    def map_to_entity(self, data, entity_type: str) -> EntityBase:
       if entity_type == "User":
           return self._user_dto_to_user(data)
       elif entity_type == "Post":
           return self._post_dto_to_post(data)
       elif entity_type == "Comment":
           return self._comment_dto_to_comment(data)

    # маппинг модели пользователя в сущность
    @staticmethod
    def _user_dto_to_user(user_data: dict):
        birthday = None if user_data.get("birthday") is None else datetime.strptime(user_data.get("birthday").split('T')[0], "%Y-%m-%d")
        gender = -1 if user_data.get("gender") is None else int(user_data.get("gender"))
        return User(
            first_name=user_data.get("firstName"),
            last_name=user_data.get("lastName"),
            gender=gender,
            registration_date=datetime.strptime(user_data.get("registrationDate").split('T')[0], "%Y-%m-%d"),
            birthday=birthday,
            education_info=user_data.get('educationInfo')
        )

    # маппинг модели комментария в сущность
    @staticmethod
    def _comment_dto_to_comment(comment_data: dict):
        parent_id = comment_data.get("parentId")
        parent_id = None if isinstance(parent_id, dict) and parent_id['@xsi:nil'] == 'true' else parent_id
        return Comment(
            content=comment_data.get("content"),
            user_id=comment_data.get("userId"),
            post_id=comment_data.get("postId"),
            parent_id=parent_id
        )

    # маппинг модели поста в сущность
    @staticmethod
    def _post_dto_to_post(post_data: dict):
        return  Post(
            title=post_data.get("title"),
            content=post_data.get("content"),
            publisher_name=post_data.get("publisherName"),
            link_url=post_data.get("linkUrl"),
            link_name=post_data.get("linkName"),
            geo_tag=post_data.get("geoTag")
        )