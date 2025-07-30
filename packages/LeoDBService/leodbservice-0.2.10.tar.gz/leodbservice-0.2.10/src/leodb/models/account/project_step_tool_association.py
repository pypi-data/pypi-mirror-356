from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from ..account_base import account_metadata

project_step_tool_association = Table(
    "project_step_tool_association",
    account_metadata,
    Column("project_step_id", UUID(as_uuid=True), ForeignKey("project_step.id", ondelete="CASCADE"), primary_key=True),
    Column("tool_use_spec_id", UUID(as_uuid=True), ForeignKey("tool_use_spec.id", ondelete="CASCADE"), primary_key=True),
)