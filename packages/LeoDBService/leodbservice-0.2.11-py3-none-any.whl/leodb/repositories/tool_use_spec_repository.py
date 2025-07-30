from sqlalchemy.ext.asyncio import AsyncSession
from leodb.models.account.tool_use_spec import ToolUseSpec
from leodb.schemas.tool_use_spec import ToolUseSpecCreate, ToolUseSpecUpdate, ToolUseSpecSchema
from .base_repository import BaseRepository

class ToolUseSpecRepository(BaseRepository[ToolUseSpec, ToolUseSpecCreate, ToolUseSpecUpdate, ToolUseSpecSchema]):
    
    def __init__(self, db: AsyncSession, model: type[ToolUseSpec]):
        super().__init__(db, model, ToolUseSpecSchema)