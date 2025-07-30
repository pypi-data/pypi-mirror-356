import asyncio
from typing import Dict, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from leodb.core.config import settings
from leodb.models.general.account_data_connection import AccountDataConnection


class DatabaseConnectionManager:
    """
    Manages database connections for a multi-tenant environment.
    """

    def __init__(self):
        self._engines: Dict[str, AsyncEngine] = {}
        self._lock = asyncio.Lock()
        # The default engine for the shared 'general' schema
        self._default_engine = create_async_engine(settings.DATABASE_URL, future=True)
        self._engines["default"] = self._default_engine
        self._default_session_factory = sessionmaker(
            self._default_engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_engine(self, account_uuid: Optional[str] = None) -> AsyncEngine:
        """
        Retrieves or creates a database engine for a specific account.
        If account_uuid is None, returns the default engine.
        """
        if not account_uuid:
            return self._default_engine

        async with self._lock:
            if account_uuid in self._engines:
                return self._engines[account_uuid]

            # If not cached, create a new engine
            session = self._default_session_factory()
            try:
                stmt = select(AccountDataConnection).where(AccountDataConnection.account_id == account_uuid)
                result = await session.execute(stmt)
                conn_details = result.scalar_one_or_none()

                if not conn_details or not all([conn_details.db_host, conn_details.db_port, conn_details.db_name, conn_details.db_user, conn_details.db_password]):
                    # Fallback to default engine if connection details are incomplete
                    return self._default_engine

                db_url = (
                    f"postgresql+asyncpg://{conn_details.db_user}:{conn_details.db_password}@"
                    f"{conn_details.db_host}:{conn_details.db_port}/{conn_details.db_name}"
                )
                
                engine = create_async_engine(db_url, future=True)
                self._engines[account_uuid] = engine
                return engine
            finally:
                await session.close()

    def get_session_factory(self, engine: AsyncEngine) -> sessionmaker:
        """Creates a session factory for a given engine."""
        return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session(self, account_uuid: Optional[str] = None) -> AsyncSession:
        """
        Provides a database session for the specified account.
        """
        if not account_uuid:
            return self._default_session_factory()

        engine = await self.get_engine(account_uuid)
        session_factory = self.get_session_factory(engine)
        return session_factory()

    async def close_all(self):
        """Closes all cached engine connections."""
        async with self._lock:
            for engine in self._engines.values():
                await engine.dispose()
            self._engines.clear()

# Global instance
connection_manager = DatabaseConnectionManager()