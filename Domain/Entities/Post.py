import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column
from Domain.Entities.Base.EntityBase import EntityBase
from sqlalchemy.dialects.postgresql import UUID

# пост пользователя
class Post(EntityBase):
    __tablename__ = 'posts'
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    publisher_name: Mapped[str] = mapped_column(String)
    link_url: Mapped[str] = mapped_column(String)
    link_name: Mapped[str] = mapped_column(String)
    geo_tag: Mapped[str] = mapped_column(String)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=False, default=uuid.uuid4)

    def __init__(self, title: str, content: str, publisher_name: str,
                 link_url: str, link_name: str, geo_tag: str):
        super().__init__()
        self.title = title
        self.content = content
        self.publisher_name = publisher_name
        self.link_url = link_url
        self.link_name = link_name
        self.geo_tag = geo_tag
