from sqlalchemy.ext.asyncio import AsyncSession
from leodb.models.account.data_source import DataSource
from leodb.schemas.data_source import DataSourceCreate, DataSourceUpdate, DataSourceSchema
from .base_repository import BaseRepository

class DataSourceRepository(BaseRepository[DataSource, DataSourceCreate, DataSourceUpdate, DataSourceSchema]):
    
    def __init__(self, db: AsyncSession, model: type[DataSource]):
        super().__init__(db, model, DataSourceSchema)