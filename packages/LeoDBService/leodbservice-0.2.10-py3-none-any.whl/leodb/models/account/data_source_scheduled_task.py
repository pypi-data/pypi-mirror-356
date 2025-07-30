from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from ..account_base import account_metadata

data_source_scheduled_task = Table(
    "data_source_scheduled_task",
    account_metadata,
    Column("scheduled_task_id", UUID(as_uuid=True), ForeignKey("scheduled_task.id", ondelete="CASCADE"), primary_key=True),
    Column("data_source_id", UUID(as_uuid=True), ForeignKey("data_source.id", ondelete="CASCADE"), primary_key=True),
)