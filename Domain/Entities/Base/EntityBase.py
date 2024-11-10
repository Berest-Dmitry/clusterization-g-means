import uuid
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase, declarative_base, Mapped
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


# класс базовой сущности проекта
class EntityBase(Base):
    __abstract__ = True
    id: Mapped[uuid] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    def __init__(self):
        self.id = uuid.uuid4()