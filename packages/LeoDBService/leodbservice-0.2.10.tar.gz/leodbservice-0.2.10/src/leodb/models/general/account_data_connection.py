import uuid
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from leodb.models.base import Base
from leodb.encryption.types import EncryptedString

class AccountDataConnection(Base):
    __tablename__ = "account_data_connections"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False, index=True
    )
    
    # Connection details
    db_host: Mapped[str] = mapped_column(EncryptedString, nullable=True)
    db_port: Mapped[int] = mapped_column(Integer, nullable=True)
    db_name: Mapped[str] = mapped_column(EncryptedString, nullable=True)
    db_user: Mapped[str] = mapped_column(EncryptedString, nullable=True)
    db_password: Mapped[str] = mapped_column(EncryptedString, nullable=True)
    vector_store_url: Mapped[str] = mapped_column(EncryptedString, nullable=True)
    vector_store_key: Mapped[str] = mapped_column(EncryptedString, nullable=True)

    # Relationships
    account: Mapped["Account"] = relationship(back_populates="data_connection")

    def __repr__(self):
        return f"<AccountDataConnection(id={self.id}, account_id={self.account_id})>"