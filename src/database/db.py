import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from src.config.config import config


class DatabaseSessionManager:
    def __init__(self, url: str):
        """
        Initialize the database session manager.
        Parameters:
        - url (str): Database URL.

        """
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        """
        Context manager for managing database sessions.
        It creates a new session, yields it, and handles exceptions.
        If an exception occurs, it rolls back the session and closes it.
        """
        if self._session_maker is None:
            raise Exception("Database session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    """
    Dependency that get a database session.
    """
    async with sessionmanager.session() as session:
        yield session
