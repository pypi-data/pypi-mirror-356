from typing import Optional
from uuid import UUID

from sqlalchemy import select

from leodb.models.general.package import Package
from .base_repository import BaseRepository

class PackageRepository(BaseRepository[Package, None, None]):

    async def get_active_for_account(self, *, account_id: UUID) -> Optional[Package]:
        """
        Retrieves the active package for a specific account.
        This assumes there is a way to identify the 'active' package,
        for example, a boolean flag or a status field.
        Let's assume a field 'is_active' for this example.
        """
        statement = (
            select(self.model)
            .where(self.model.account_id == account_id)
            .where(self.model.is_active == True) # Assuming an 'is_active' flag
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()