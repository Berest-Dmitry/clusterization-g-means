import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy.testing.schema import mapped_column

Base = declarative_base()


# класс базовой сущности проекта
class EntityBase(AsyncAttrs, Base):
    __abstract__ = True
    id: Mapped[uuid] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    def __init__(self):
        self.id = uuid.uuid4()