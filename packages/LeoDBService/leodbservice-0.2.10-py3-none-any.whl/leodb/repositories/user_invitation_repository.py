from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from leodb.models.general.user_invitation import UserInvitation
from leodb.schemas.user_invitation import UserInvitationCreate, UserInvitationSchema
from .base_repository import BaseRepository

class UserInvitationRepository(BaseRepository[UserInvitation, UserInvitationCreate, None, UserInvitationSchema]):

    def __init__(self, db: AsyncSession, model: type[UserInvitation]):
        super().__init__(db, model, UserInvitationSchema)

    async def create_invitation(self, *, obj_in: UserInvitationCreate) -> UserInvitationSchema:
        return await self.create(obj_in=obj_in)

    async def get_by_account(self, *, account_id: UUID) -> List[UserInvitationSchema]:
        statement = select(self.model).where(self.model.account_id == account_id)
        result = await self.db.execute(statement)
        db_objs = result.scalars().all()
        return [self.read_schema.from_orm(db_obj) for db_obj in db_objs]