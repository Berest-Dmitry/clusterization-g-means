import string
from typing import Optional, Literal

from pydantic.v1 import UUID4
from pydantic_xml import BaseXmlModel, attr


class CommentClusteringModel(BaseXmlModel):
    content: Literal[string] = attr()
    user_id: Literal[UUID4] = attr()
    post_id: Literal[UUID4] = attr()
    parent_id: Literal[UUID4] = attr()
