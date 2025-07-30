from typing import List, Tuple
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from leodb.models.general.invoice import Invoice
from leodb.schemas.billing import InvoiceDetailSchema
from .base_repository import BaseRepository

class InvoiceRepository(BaseRepository[Invoice, None, None, InvoiceDetailSchema]):

    def __init__(self, db: AsyncSession, model: type[Invoice]):
        super().__init__(db, model, InvoiceDetailSchema)

    async def get_by_account_paginated(
        self, *, account_id: UUID, skip: int = 0, limit: int = 100
    ) -> Tuple[int, List[InvoiceDetailSchema]]:
        count_statement = select(func.count()).select_from(self.model).where(self.model.account_id == account_id)
        total = (await self.db.execute(count_statement)).scalar_one()

        statement = (
            select(self.model)
            .where(self.model.account_id == account_id)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.created_at.desc())
        )
        result = await self.db.execute(statement)
        db_objs = result.scalars().all()
        return total, [self.read_schema.from_orm(db_obj) for db_obj in db_objs]