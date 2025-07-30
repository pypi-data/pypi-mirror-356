from sqlalchemy.ext.asyncio import AsyncSession
from leodb.models.account.record import Record
from leodb.schemas.record import RecordCreate, RecordUpdate, RecordSchema
from .base_repository import BaseRepository

class RecordRepository(BaseRepository[Record, RecordCreate, RecordUpdate, RecordSchema]):
    
    def __init__(self, db: AsyncSession, model: type[Record]):
        super().__init__(db, model, RecordSchema)