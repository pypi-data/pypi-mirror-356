import uuid
from sqlalchemy import Column, String, TIMESTAMP, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..base import Base
from ..account_base import account_metadata

class ToolUseSpec(Base):
    __tablename__ = "tool_use_spec"
    __table_args__ = {"metadata": account_metadata}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tool_name = Column(String, nullable=False)
    spec = Column(JSON, nullable=False)
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())