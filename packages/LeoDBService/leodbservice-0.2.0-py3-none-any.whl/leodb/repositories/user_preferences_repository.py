from typing import Optional
from uuid import UUID

from sqlalchemy import select

from leodb.models.general.user_preferences import UserPreferences
from leodb.schemas.user_preferences import UserPreferencesCreate, UserPreferencesUpdate # Schémas à créer
from .base_repository import BaseRepository

class UserPreferencesRepository(BaseRepository[UserPreferences, UserPreferencesCreate, UserPreferencesUpdate]):

    async def get_by_user_id(self, *, user_id: UUID) -> Optional[UserPreferences]:
        """
        Finds preferences by user ID.
        """
        statement = select(self.model).where(self.model.user_id == user_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create_for_user(self, *, user_id: UUID, obj_in: UserPreferencesCreate) -> UserPreferences:
        """
        Creates preferences for a specific user.
        """
        # Assure que l'ID de l'utilisateur est bien celui fourni, et non celui du schéma
        create_data = obj_in.model_dump()
        create_data["user_id"] = user_id
        
        db_obj = self.model(**create_data)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj