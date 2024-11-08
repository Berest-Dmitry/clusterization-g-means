from sqlalchemy import Column, String
from Domain.Entities.Base.EntityBase import EntityBase


# пост пользователя
class Post(EntityBase):
    __tablename__ = 'posts'
    title: str = Column(String, nullable=False)
    content: str = Column(String, nullable=False)
    publisher_name: str = Column(String)
    link_url: str = Column(String)
    link_name: str = Column(String)
    geo_tag: str = Column(String)

    def __init__(self, title: str, content: str, publisher_name: str,
                 link_url: str, link_name: str, geo_tag: str):
        super().__init__()
        self.title = title
        self.content = content
        self.publisher_name = publisher_name
        self.link_url = link_url
        self.link_name = link_name
        self.geo_tag = geo_tag
