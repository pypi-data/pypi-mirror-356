from typing import List, Tuple
from uuid import UUID

from sqlalchemy import select, func

from leodb.models.general.invoice import Invoice
from .base_repository import BaseRepository

class InvoiceRepository(BaseRepository[Invoice, None, None]):

    async def get_by_account_paginated(
        self, *, account_id: UUID, skip: int = 0, limit: int = 100
    ) -> Tuple[int, List[Invoice]]:
        """
        Lists invoices for a specific account with pagination.
        Returns a tuple of (total_invoices, list_of_invoices).
        """
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
        invoices = result.scalars().all()
        return total, invoices