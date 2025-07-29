from typing import Optional
from uuid import UUID

from sqlalchemy import select

from leodb.models.general.payment_method import PaymentMethod
from leodb.schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate # Schémas à créer
from .base_repository import BaseRepository

class PaymentMethodRepository(BaseRepository[PaymentMethod, PaymentMethodCreate, PaymentMethodUpdate]):

    async def get_by_account(self, *, account_id: UUID) -> Optional[PaymentMethod]:
        """
        Finds the payment method for a specific account.
        Assumes one payment method per account for simplicity.
        """
        statement = select(self.model).where(self.model.account_id == account_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create_or_update(
        self, *, account_id: UUID, obj_in: PaymentMethodCreate
    ) -> PaymentMethod:
        """
        Creates a new payment method or updates the existing one for an account.
        """
        db_obj = await self.get_by_account(account_id=account_id)
        if db_obj:
            # Update existing payment method
            update_data = obj_in.model_dump(exclude_unset=True)
            return await self.update(db_obj=db_obj, obj_in=update_data)
        else:
            # Create new payment method
            create_data = obj_in.model_dump()
            create_data["account_id"] = account_id
            return await self.create(obj_in=PaymentMethodCreate(**create_data))