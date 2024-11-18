from uuid import UUID, uuid4
from typing import Optional
import pydantic
from pydantic_xml import BaseXmlModel, attr


class CommentClusteringModel(BaseXmlModel):
    content: Optional[str] = attr()
    user_id: Optional[UUID] = pydantic.Field(default_factory=uuid4)
    post_id: Optional[UUID] = pydantic.Field(default_factory=uuid4)
    parent_id: Optional[UUID] = pydantic.Field(default_factory=uuid4)

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data['user_id'] = str(self.user_id)
        data['post_id'] = str(self.post_id)
        data['parent_id'] = str(self.parent_id)
        return data
