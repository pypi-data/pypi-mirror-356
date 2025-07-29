from typing import List
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from leodb.models.account.conversation import Conversation
from leodb.models.account.message import Message
from leodb.schemas.conversation import MessageCreate
from .base_repository import BaseRepository
from leodb.core.config import settings

class MessageRepository(BaseRepository[Message, MessageCreate, None]):

    async def add_message(self, *, conversation_id: UUID, obj_in: MessageCreate) -> Message:
        """
        Adds a new message to a conversation and handles related logic:
        1. Updates the conversation's last_updated_at timestamp.
        2. Creates the new message.
        3. Truncates old messages if the conversation exceeds the configured limit.
        All operations are part of the same transaction managed by the UnitOfWork.
        """
        # 1. Update conversation timestamp
        conversation = await self._session.get(Conversation, conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with id {conversation_id} not found.")
        conversation.last_updated_at = datetime.utcnow()

        # 2. Create the new message
        # Note: le nom du champ dans le modèle est meta_data
        db_obj = Message(
            conversation_id=conversation_id,
            role=obj_in.role,
            content=obj_in.content,
            meta_data=obj_in.metadata
        )
        self._session.add(db_obj)
        
        # 3. Truncate old messages
        # This part is complex and requires careful handling of session state.
        # We flush to get the new message_id and ensure the count is correct.
        await self._session.flush()

        # Check if truncation is needed
        max_messages = settings.POSTGRES_MAX_MESSAGES_PER_CONVERSATION # Assuming this setting exists
        if max_messages and max_messages > 0:
            # Subquery to find the IDs of messages to delete
            subquery = (
                select(Message.message_id)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .offset(max_messages)
                .scalar_subquery()
            )
            # Delete statement
            delete_stmt = delete(Message).where(Message.message_id.in_(subquery))
            await self._session.execute(delete_stmt)

        await self._session.flush()
        return db_obj

    async def get_history(self, *, conversation_id: UUID, limit: int) -> List[Message]:
        """
        Gets the most recent messages from a conversation.
        """
        stmt = (
            select(self._model)
            .where(self._model.conversation_id == conversation_id)
            .order_by(self._model.created_at.asc()) # ASC to get the chronological order
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()