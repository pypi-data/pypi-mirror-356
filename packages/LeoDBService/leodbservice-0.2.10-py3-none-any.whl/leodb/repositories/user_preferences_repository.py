from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from leodb.models.general.user_preferences import UserPreferences
from leodb.schemas.user_preferences import UserPreferencesCreate, UserPreferencesUpdate, UserPreferencesSchema
from .base_repository import BaseRepository

class UserPreferencesRepository(BaseRepository[UserPreferences, UserPreferencesCreate, UserPreferencesUpdate, UserPreferencesSchema]):

    def __init__(self, db: AsyncSession, model: type[UserPreferences]):
        super().__init__(db, model, UserPreferencesSchema)

    async def get_by_user_id(self, *, user_id: UUID) -> Optional[UserPreferencesSchema]:
        statement = select(self.model).where(self.model.user_id == user_id)
        result = await self.db.execute(statement)
        db_obj = result.scalar_one_or_none()
        return self.read_schema.from_orm(db_obj) if db_obj else None

    async def create_for_user(self, *, user_id: UUID, obj_in: UserPreferencesCreate) -> UserPreferencesSchema:
        create_data = obj_in.model_dump()
        create_data["user_id"] = user_id
        
        db_obj = self.model(**create_data)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return self.read_schema.from_orm(db_obj)