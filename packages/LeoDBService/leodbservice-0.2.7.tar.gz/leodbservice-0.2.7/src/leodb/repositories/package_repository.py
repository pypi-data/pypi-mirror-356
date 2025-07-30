from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from leodb.models.general.package import Package
from leodb.schemas.billing import SubscriptionSchema
from .base_repository import BaseRepository

class PackageRepository(BaseRepository[Package, None, None, SubscriptionSchema]):

    def __init__(self, db: AsyncSession, model: type[Package]):
        super().__init__(db, model, SubscriptionSchema)

    async def get_active_for_account(self, *, account_id: UUID) -> Optional[SubscriptionSchema]:
        statement = (
            select(self.model)
            .where(self.model.account_id == account_id)
            .where(self.model.is_active == True)
        )
        result = await self.db.execute(statement)
        db_obj = result.scalar_one_or_none()
        return self.read_schema.from_orm(db_obj) if db_obj else None