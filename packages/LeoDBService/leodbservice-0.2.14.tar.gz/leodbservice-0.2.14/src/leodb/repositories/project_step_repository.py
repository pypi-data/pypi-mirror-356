from sqlalchemy.ext.asyncio import AsyncSession
from leodb.models.account.project_step import ProjectStep
from leodb.schemas.project_step import ProjectStepCreate, ProjectStepUpdate, ProjectStepSchema
from .base_repository import BaseRepository

class ProjectStepRepository(BaseRepository[ProjectStep, ProjectStepCreate, ProjectStepUpdate, ProjectStepSchema]):
    
    def __init__(self, db: AsyncSession, model: type[ProjectStep]):
        super().__init__(db, model, ProjectStepSchema)