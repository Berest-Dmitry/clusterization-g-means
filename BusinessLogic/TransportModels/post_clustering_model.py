import uuid
from typing import Optional
from pydantic_xml import attr, BaseXmlModel


class PostClusteringModel(BaseXmlModel):
    title: Optional[str] = attr()
    content: Optional[str] = attr()
    publisher_name: Optional[str] = attr()
    link_url: Optional[str] = attr()
    link_name: Optional[str] = attr()
    geo_tag: Optional[str] = attr()
    user_id: Optional[uuid.UUID] = attr(default_factory=uuid.uuid4)

