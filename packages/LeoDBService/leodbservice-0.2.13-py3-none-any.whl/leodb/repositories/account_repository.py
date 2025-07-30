from sqlalchemy.ext.asyncio import AsyncSession
from leodb.models.general.account import Account
from leodb.schemas.account import AccountCreate, AccountUpdate, AccountSchema
from .base_repository import BaseRepository

class AccountRepository(BaseRepository[Account, AccountCreate, AccountUpdate, AccountSchema]):
    def __init__(self, db: AsyncSession, model: type[Account]):
        super().__init__(db, model, AccountSchema)