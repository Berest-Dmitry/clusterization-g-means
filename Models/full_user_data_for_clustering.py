import string
from typing import List
from PyQt5.uic.Compiler.misc import Literal
from pydantic_xml import BaseXmlModel, element, attr
from Models.comment_clustering_model import CommentClusteringModel
from Models.post_clustering_model import PostClusteringModel


class FullUserDataForClustering(BaseXmlModel):
    first_name: Literal[string] = attr()
    last_name:  Literal[string] = attr()
    birthday:  Literal[string] = attr()
    gender: Literal[string] = attr()
    education_info:  Literal[string] = attr()
    registration_date: Literal[string] = attr()
    userPosts: List[PostClusteringModel] = element(tag="user_posts", default=[])
    userComments: List[CommentClusteringModel] = element(tag="user_comments", default=[])
