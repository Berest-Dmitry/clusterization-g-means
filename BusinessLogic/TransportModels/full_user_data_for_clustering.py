import datetime
import uuid
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr
from BusinessLogic.TransportModels.comment_clustering_model import CommentClusteringModel
from BusinessLogic.TransportModels.post_clustering_model import PostClusteringModel


class FullUserDataForClustering(BaseXmlModel):
    first_name: Optional[str] = attr()
    last_name:  Optional[str] = attr()
    birthday:  Optional[datetime.datetime] = attr(default=None)
    gender: Optional[str] = attr()
    education_info:  Optional[str] = attr()
    registration_date: Optional[str] = attr()
    outer_service_id: Optional[uuid.UUID] = attr(default_factory=uuid.uuid4)
    userPosts: Optional[List[PostClusteringModel]] = element(tag="user_posts", default=[])
    userComments: Optional[List[CommentClusteringModel]] = element(tag="user_comments", default=[])
