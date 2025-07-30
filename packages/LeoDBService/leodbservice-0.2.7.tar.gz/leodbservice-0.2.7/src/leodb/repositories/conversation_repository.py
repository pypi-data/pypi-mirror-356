from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from leodb.models.account.conversation import Conversation
from leodb.models.account.message import Message
from leodb.schemas.conversation import ConversationCreate, ConversationUpdate, ConversationInfo
from .base_repository import BaseRepository

class ConversationRepository(BaseRepository[Conversation, ConversationCreate, ConversationUpdate, ConversationInfo]):

    def __init__(self, db: AsyncSession, model: type[Conversation]):
        super().__init__(db, model, ConversationInfo)
    
    async def create(self, *, obj_in: ConversationCreate) -> ConversationInfo:
        # Note: le nom du champ dans le modèle est meta_data
        db_obj = Conversation(
            user_id=obj_in.user_id,
            client_type=obj_in.client_type,
            client_version=obj_in.client_version,
            title=obj_in.title,
            meta_data=obj_in.metadata
        )
        self._session.add(db_obj)
        await self._session.flush()
        await self._session.refresh(db_obj)
        return self.read_schema.from_orm(db_obj)

    async def get_all_by_user(self, *, user_id: str, limit: int = 100) -> List[ConversationInfo]:
        """
        Lists conversations for a user, returning only their ID and title.
        """
        stmt = (
            select(Conversation.conversation_id, Conversation.title)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.last_updated_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        # Les résultats sont des tuples (id, title), on les mappe vers le schéma
        return [ConversationInfo(conversation_id=row.conversation_id, title=row.title) for row in result]

    async def update_title(self, *, conversation_id: UUID, title: str) -> Optional[ConversationInfo]:
        # We need the model object to update it, not the schema from self.get()
        statement = select(self.model).where(self.model.conversation_id == conversation_id)
        result = await self._session.execute(statement)
        db_obj = result.scalar_one_or_none()

        if db_obj:
            db_obj.title = title
            self._session.add(db_obj)
            await self._session.flush()
            await self._session.refresh(db_obj)
            return self.read_schema.from_orm(db_obj)
        return None

    async def clean_old_conversations(self, *, max_age_days: int) -> int:
        cutoff_date = datetime.utcnow() - timedelta(days=max_age_days)
        stmt = Conversation.__table__.delete().where(Conversation.last_updated_at < cutoff_date)
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.rowcount