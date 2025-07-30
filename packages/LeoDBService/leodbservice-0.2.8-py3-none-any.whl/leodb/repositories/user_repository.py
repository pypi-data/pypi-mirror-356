from typing import Optional, List, Tuple, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from leodb.models.general.user import User
from leodb.schemas.user import UserCreate, UserUpdate, UserSchema
from .base_repository import BaseRepository

class UserRepository(BaseRepository[User, UserCreate, UserUpdate, UserSchema]):
    
    def __init__(self, db: AsyncSession, model: type[User]):
        super().__init__(db, model, UserSchema)

    async def get_by_email(self, *, email: str) -> Optional[UserSchema]:
        statement = select(self.model).where(self.model.email == email)
        result = await self.db.execute(statement)
        db_obj = result.scalar_one_or_none()
        return self.read_schema.from_orm(db_obj) if db_obj else None

    async def get_by_entra_id(self, *, entra_id: str) -> Optional[UserSchema]:
        statement = select(self.model).where(self.model.entra_id == entra_id)
        result = await self.db.execute(statement)
        db_obj = result.scalar_one_or_none()
        return self.read_schema.from_orm(db_obj) if db_obj else None

    async def get_by_account_paginated(
        self, *, account_id: UUID, skip: int = 0, limit: int = 100
    ) -> Tuple[int, List[UserSchema]]:
        count_statement = select(func.count()).select_from(self.model).where(self.model.account_id == account_id)
        total = (await self.db.execute(count_statement)).scalar_one()

        statement = (
            select(self.model)
            .where(self.model.account_id == account_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(statement)
        db_objs = result.scalars().all()
        return total, [self.read_schema.from_orm(db_obj) for db_obj in db_objs]

    async def add_to_account(self, *, user: User, account_id: UUID) -> UserSchema:
        user.account_id = account_id
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return self.read_schema.from_orm(user)

    async def remove_from_account(self, *, user: User) -> UserSchema:
        user.account_id = None
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return self.read_schema.from_orm(user)

    async def sync_from_azure(self, *, azure_user_data: Dict[str, Any]) -> UserSchema:
        """
        Finds a user by their entra_id and updates them, or creates them if they don't exist.
        """
        entra_id = azure_user_data.get("entra_id")
        if not entra_id:
            raise ValueError("entra_id is required in azure_user_data")

        # We need the model object to perform an update
        statement = select(self.model).where(self.model.entra_id == entra_id)
        result = await self.db.execute(statement)
        db_obj = result.scalar_one_or_none()

        if db_obj:
            # User exists, update them
            return await self.update(db_obj=db_obj, obj_in=azure_user_data)
        else:
            # User does not exist, create them
            user_in = UserCreate(**azure_user_data)
            return await self.create(obj_in=user_in)

    async def activate(self, *, user: User, activation_data: Dict[str, Any]) -> UserSchema:
        update_data = {"status": "ACTIVE", **activation_data}
        return await self.update(db_obj=user, obj_in=update_data)

    async def reject(self, *, user: User, rejection_data: Dict[str, Any]) -> UserSchema:
        update_data = {"status": "REJECTED", **rejection_data}
        return await self.update(db_obj=user, obj_in=update_data)

    async def update_last_login(self, *, user: User) -> UserSchema:
        return await self.update(db_obj=user, obj_in={"last_login_at": datetime.utcnow()})