from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from leodb.models.account.conversation import Conversation
from leodb.models.account.message import Message
from leodb.schemas.conversation import ConversationCreate, ConversationUpdate, ConversationWithStats, ConversationInfo
from .base_repository import BaseRepository

class ConversationRepository(BaseRepository[Conversation, ConversationCreate, ConversationUpdate]):
    
    async def create(self, *, obj_in: ConversationCreate) -> Conversation:
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
        return db_obj

    async def get_info(self, conversation_id: UUID) -> Optional[ConversationInfo]:
        stmt = (
            select(
                Conversation,
                func.count(Message.message_id).label("message_count")
            )
            .outerjoin(Message, Conversation.conversation_id == Message.conversation_id)
            .where(Conversation.conversation_id == conversation_id)
            .group_by(Conversation.conversation_id)
        )
        result = await self._session.execute(stmt)
        row = result.one_or_none()
        if row:
            conv, count = row
            conv_info = ConversationInfo.from_orm(conv)
            conv_info.message_count = count
            return conv_info
        return None

    async def get_all_by_user(self, *, user_id: str, limit: int = 10) -> List[ConversationWithStats]:
        last_user_message_subquery = (
            select(Message.content)
            .where(Message.conversation_id == Conversation.conversation_id)
            .where(Message.role == 'user')
            .order_by(Message.created_at.desc())
            .limit(1)
            .correlate(Conversation)
            .as_scalar()
        )

        stmt = (
            select(
                Conversation,
                func.count(Message.message_id).label("message_count"),
                last_user_message_subquery.label("last_user_message")
            )
            .outerjoin(Message, Conversation.conversation_id == Message.conversation_id)
            .where(Conversation.user_id == user_id)
            .group_by(Conversation.conversation_id)
            .order_by(Conversation.last_updated_at.desc())
            .limit(limit)
        )
        
        result = await self._session.execute(stmt)
        
        conversations_with_stats = []
        for row in result.all():
            conv, count, last_msg = row
            stat = ConversationWithStats.from_orm(conv)
            stat.message_count = count
            stat.last_user_message = last_msg
            conversations_with_stats.append(stat)
            
        return conversations_with_stats

    async def update_title(self, *, conversation_id: UUID, title: str) -> Optional[Conversation]:
        db_obj = await self.get(conversation_id)
        if db_obj:
            db_obj.title = title
            await self._session.flush()
        return db_obj

    async def clean_old_conversations(self, *, max_age_days: int) -> int:
        cutoff_date = datetime.utcnow() - timedelta(days=max_age_days)
        stmt = Conversation.__table__.delete().where(Conversation.last_updated_at < cutoff_date)
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.rowcount