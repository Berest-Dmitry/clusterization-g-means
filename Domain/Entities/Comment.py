import uuid
from sqlalchemy.dialects.postgresql import UUID
from Domain.Entities.Base.EntityBase import EntityBase
from sqlalchemy import  Column, String

# сущность комментария пользователя
class Comment(EntityBase):
    __tablename__ = 'comments'
    content: str = Column(String(500), nullable=False)
    user_id: uuid = Column(UUID(as_uuid=True), primary_key=False, default=uuid.uuid4)
    post_id: uuid = Column(UUID(as_uuid=True), primary_key=False, default=uuid.uuid4)
    parent_id: uuid = Column(UUID(as_uuid=True), primary_key=False, default=uuid.uuid4)

    def __init__(self, content: str, user_id: uuid, post_id: uuid, parent_id: uuid):
        super().__init__()
        self.content = content
        self.user_id = user_id
        self.post_id = post_id
        self.parent_id = parent_id

