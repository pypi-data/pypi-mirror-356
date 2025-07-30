from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from leodb.models.general.payment_method import PaymentMethod
from leodb.schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodSchema
from .base_repository import BaseRepository

class PaymentMethodRepository(BaseRepository[PaymentMethod, PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodSchema]):

    def __init__(self, db: AsyncSession, model: type[PaymentMethod]):
        super().__init__(db, model, PaymentMethodSchema)

    async def get_by_account(self, *, account_id: UUID) -> Optional[PaymentMethodSchema]:
        statement = select(self.model).where(self.model.account_id == account_id)
        result = await self.db.execute(statement)
        db_obj = result.scalar_one_or_none()
        return self.read_schema.from_orm(db_obj) if db_obj else None

    async def create_or_update(
        self, *, account_id: UUID, obj_in: PaymentMethodCreate
    ) -> PaymentMethodSchema:
        # We need the model object to perform an update
        statement = select(self.model).where(self.model.account_id == account_id)
        result = await self.db.execute(statement)
        db_obj = result.scalar_one_or_none()

        if db_obj:
            # Update existing payment method
            update_data = obj_in.model_dump(exclude_unset=True)
            return await self.update(db_obj=db_obj, obj_in=update_data)
        else:
            # Create new payment method
            create_data = obj_in.model_dump()
            create_data["account_id"] = account_id
            # The base create method expects a Pydantic schema
            create_schema = PaymentMethodCreate(**create_data)
            return await self.create(obj_in=create_schema)