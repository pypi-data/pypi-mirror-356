from sqlalchemy.ext.asyncio import AsyncSession
from leodb.models.account.project_output import ProjectOutput
from leodb.schemas.project_output import ProjectOutputCreate, ProjectOutputUpdate, ProjectOutputSchema
from .base_repository import BaseRepository

class ProjectOutputRepository(BaseRepository[ProjectOutput, ProjectOutputCreate, ProjectOutputUpdate, ProjectOutputSchema]):
    
    def __init__(self, db: AsyncSession, model: type[ProjectOutput]):
        super().__init__(db, model, ProjectOutputSchema)