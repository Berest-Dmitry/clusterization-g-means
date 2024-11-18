from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from BusinessLogic.Services.Common.ConfigLoader import get_config_section
from Domain.Entities.Base.EntityBase import Base



# контекст БД
class AppContext:
    _db_engine: AsyncEngine
    _connection_str: str
    is_initialized: bool = False

    # метод инициализации движка работы с БД
    async def init_engine(self) -> None:
        try:
            self._connection_str = get_config_section("db_connection")
            self._db_engine = create_async_engine(self._connection_str, server_side_cursors=False)
            async with self._db_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            self.is_initialized = True
        except BaseException as e:
            raise e

    # метод получения подключения к БД
    def get_async_session(self):
        return async_sessionmaker(
            bind=self._db_engine, expire_on_commit=False, class_=AsyncSession
        )
