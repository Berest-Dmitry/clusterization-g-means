import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from Domain.Entities.Base.EntityBase import EntityBase
from sqlalchemy.dialects.postgresql import UUID

# сущность пользователя
class User(EntityBase):
    __tablename__ = 'users'
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    birthday: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    gender: Mapped[int] = mapped_column(Integer, nullable=True)
    education_info: Mapped[str] = mapped_column(String)
    registration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    outer_service_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=False, default=uuid.uuid4)

    def __init__(self, first_name: str, last_name: str, birthday: datetime
                 , gender: int, education_info: str, registration_date: datetime, outer_service_id: uuid.UUID):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.education_info = education_info
        self.registration_date = registration_date
        self.outer_service_id = outer_service_id
