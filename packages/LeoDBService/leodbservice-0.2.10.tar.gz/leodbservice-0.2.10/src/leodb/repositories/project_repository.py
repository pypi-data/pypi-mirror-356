from sqlalchemy.ext.asyncio import AsyncSession
from leodb.models.account.project import Project
from leodb.schemas.project import ProjectCreate, ProjectUpdate, ProjectSchema
from .base_repository import BaseRepository

class ProjectRepository(BaseRepository[Project, ProjectCreate, ProjectUpdate, ProjectSchema]):
    
    def __init__(self, db: AsyncSession, model: type[Project]):
        super().__init__(db, model, ProjectSchema)