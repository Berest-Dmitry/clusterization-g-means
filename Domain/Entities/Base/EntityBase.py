import uuid
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID

# класс базовой сущности проекта
class EntityBase(DeclarativeBase):
    id: uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    def __init__(self):
        self.id = uuid.uuid4()