from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from leodb.models.general.user import User
from leodb.schemas.user import UserCreate, UserUpdate
from .base_repository import BaseRepository

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    
    async def get_by_email(self, *, email: str) -> Optional[User]:
        """
        Finds a user by their email address.
        """
        statement = select(self.model).where(self.model.email == email)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_entra_id(self, *, entra_id: str) -> Optional[User]:
        """
        Finds a user by their Azure Entra ID.
        """
        statement = select(self.model).where(self.model.entra_id == entra_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_account_paginated(
        self, *, account_id: UUID, skip: int = 0, limit: int = 100
    ) -> (int, List[User]):
        """
        Lists users for a specific account with pagination.
        Returns a tuple of (total_users, list_of_users).
        """
        count_statement = select(func.count()).select_from(self.model).where(self.model.account_id == account_id)
        total = (await self.db.execute(count_statement)).scalar_one()

        statement = (
            select(self.model)
            .where(self.model.account_id == account_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(statement)
        users = result.scalars().all()
        return total, users

    async def add_to_account(self, *, user: User, account_id: UUID) -> User:
        """
        Associates an existing user with an account.
        """
        user.account_id = account_id
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_or_create_from_azure(self, *, azure_user_data: dict) -> User:
        """
        Finds a user by their entra_id or creates them if they don't exist.
        Expects azure_user_data to contain 'entra_id', 'email', 'display_name'.
        """
        entra_id = azure_user_data.get("entra_id")
        if not entra_id:
            raise ValueError("entra_id is required in azure_user_data")

        user = await self.get_by_entra_id(entra_id=entra_id)
        if not user:
            user_in = UserCreate(**azure_user_data)
            user = await self.create(obj_in=user_in)
        return user

    async def update_from_azure(self, *, user: User, azure_user_data: dict) -> User:
        """
        Updates a user's information from Azure data.
        """
        # We use the generic update method from the base repository.
        # The input dict can contain any fields to update.
        return await self.update(db_obj=user, obj_in=azure_user_data)

    async def activate(self, *, user: User, activation_data: dict) -> User:
        """
        Activates a user account.
        """
        update_data = {"status": "ACTIVE", **activation_data}
        return await self.update(db_obj=user, obj_in=update_data)

    async def reject(self, *, user: User, rejection_data: dict) -> User:
        """
        Rejects a user account.
        """
        update_data = {"status": "REJECTED", **rejection_data}
        return await self.update(db_obj=user, obj_in=update_data)

    async def update_last_login(self, *, user: User) -> User:
        """
        Updates the last login timestamp for a user.
        """
        from datetime import datetime
        return await self.update(db_obj=user, obj_in={"last_login_at": datetime.utcnow()})

    async def remove_from_account(self, *, user: User) -> User:
        """
        Disassociates a user from their account.
        """
        user.account_id = None
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user