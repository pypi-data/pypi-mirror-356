from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from leodb.models.general.user_session import UserSession
from leodb.schemas.user_session import UserSessionCreate, UserSessionSchema
from .base_repository import BaseRepository

class UserSessionRepository(BaseRepository[UserSession, UserSessionCreate, None, UserSessionSchema]):

    def __init__(self, db: AsyncSession, model: type[UserSession]):
        super().__init__(db, model, UserSessionSchema)

    async def create_session(self, *, obj_in: UserSessionCreate) -> UserSessionSchema:
        return await self.create(obj_in=obj_in)

    async def deactivate(self, *, session_id: UUID) -> Optional[UserSessionSchema]:
        statement = select(self.model).where(self.model.session_id == session_id)
        result = await self.db.execute(statement)
        db_obj = result.scalar_one_or_none()
        
        if db_obj:
            db_obj.is_active = False
            db_obj.deactivated_at = datetime.utcnow()
            self.db.add(db_obj)
            await self.db.flush()
            await self.db.refresh(db_obj)
            return self.read_schema.from_orm(db_obj)
        return None

    async def deactivate_all_for_user(self, *, user_id: UUID) -> int:
        stmt = (
            update(UserSession)
            .where(UserSession.user_id == user_id)
            .where(UserSession.is_active == True)
            .values(is_active=False, deactivated_at=datetime.utcnow())
        )
        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.rowcount

    async def get_active_for_user(self, *, user_id: UUID) -> List[UserSessionSchema]:
        stmt = (
            select(UserSession)
            .where(UserSession.user_id == user_id)
            .where(UserSession.is_active == True)
        )
        result = await self.db.execute(stmt)
        db_objs = result.scalars().all()
        return [self.read_schema.from_orm(db_obj) for db_obj in db_objs]