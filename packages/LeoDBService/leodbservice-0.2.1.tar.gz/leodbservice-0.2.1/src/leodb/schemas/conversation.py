from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

# ==================
# Schémas de base
# ==================

class ConversationBase(BaseModel):
    user_id: str
    client_type: Optional[str] = None
    client_version: Optional[str] = None
    title: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class MessageBase(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

# ==================
# Schémas pour la création
# ==================

class ConversationCreate(ConversationBase):
    pass

class MessageCreate(MessageBase):
    pass

# ==================
# Schémas pour la mise à jour
# ==================

class ConversationUpdate(BaseModel):
    title: Optional[str] = None

# ==================
# Schémas pour la lecture (depuis la DB)
# ==================

class MessageRead(MessageBase):
    message_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationInfo(ConversationBase):
    conversation_id: UUID
    created_at: datetime
    last_updated_at: datetime
    message_count: int

    class Config:
        from_attributes = True

class ConversationWithStats(ConversationInfo):
    last_user_message: Optional[str] = None

    class Config:
        from_attributes = True