from typing import List, Optional
from uuid import UUID

from sqlalchemy import select

from leodb.models.general.user_invitation import UserInvitation
from leodb.schemas.user_invitation import UserInvitationCreate
from .base_repository import BaseRepository

class UserInvitationRepository(BaseRepository[UserInvitation, UserInvitationCreate, None]):

    async def create_invitation(self, *, obj_in: UserInvitationCreate) -> UserInvitation:
        """
        Creates a new invitation from a UserInvitationCreate schema.
        """
        return await self.create(obj_in=obj_in)

    async def get_by_account(self, *, account_id: UUID) -> List[UserInvitation]:
        """
        Lists all invitations for a specific account.
        """
        statement = select(self.model).where(self.model.account_id == account_id)
        result = await self.db.execute(statement)
        return result.scalars().all()