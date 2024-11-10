from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from BusinessLogic.Services.Common.ConfigLoader import get_config_section
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# контекст БД
class AppContext:
    _db_engine: AsyncEngine
    _connection_str: str

    # метод инициализации движка работы с БД
    def init_engine(self) -> None:
        self._connection_str = get_config_section("db_connection")
        self._db_engine = create_async_engine(self._connection_str)
        Base.metadata.create_all(self._db_engine)

    # метод получения подключения к БД
    def get_async_session(self):
        return async_sessionmaker(
            bind=self._db_engine, expire_on_commit=False, class_=AsyncSession
        )
