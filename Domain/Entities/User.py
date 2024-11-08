from datetime import datetime
from sqlalchemy import Column, String, DATETIME, Integer
from Domain.Entities.Base.EntityBase import EntityBase

# сущность пользователя
class User(EntityBase):
    __tablename__ = 'users'
    first_name: str = Column(String(50), nullable=False)
    last_name: str = Column(String(50), nullable=False)
    birthday: datetime = Column(DATETIME, nullable=True)
    gender: int = Column(Integer, nullable=True)
    education_info: str = Column(String)
    registration_date: datetime = Column(DATETIME, nullable=False)

    def __init__(self, first_name: str, last_name: str, birthday: datetime
                 , gender: int, education_info: str, registration_date: datetime):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.education_info = education_info
        self.registration_date = registration_date
