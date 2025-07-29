from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, update
from fastapi import Request

from leodb.models.general.user_session import UserSession
from leodb.schemas.user_session import UserSessionCreate, UserSessionSchema
from .base_repository import BaseRepository

class UserSessionRepository(BaseRepository[UserSession, UserSessionCreate, None]):

    async def create_session(self, *, obj_in: UserSessionCreate) -> UserSession:
        """
        Creates a new session for a user from a UserSessionCreate schema.
        """
        # The base 'create' method is sufficient if the schema matches the model fields.
        return await self.create(obj_in=obj_in)

    async def deactivate(self, *, session_id: UUID) -> Optional[UserSession]:
        """
        Deactivates a specific session.
        """
        session = await self.get(session_id)
        if session:
            session.is_active = False
            session.deactivated_at = datetime.utcnow()
            self.db.add(session)
            await self.db.flush()
            await self.db.refresh(session)
        return session

    async def deactivate_all_for_user(self, *, user_id: UUID) -> int:
        """
        Deactivates all active sessions for a specific user.
        """
        stmt = (
            update(UserSession)
            .where(UserSession.user_id == user_id)
            .where(UserSession.is_active == True)
            .values(is_active=False, deactivated_at=datetime.utcnow())
        )
        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.rowcount

    async def get_active_for_user(self, *, user_id: UUID) -> List[UserSession]:
        """
        Gets all active sessions for a user.
        """
        stmt = (
            select(UserSession)
            .where(UserSession.user_id == user_id)
            .where(UserSession.is_active == True)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()