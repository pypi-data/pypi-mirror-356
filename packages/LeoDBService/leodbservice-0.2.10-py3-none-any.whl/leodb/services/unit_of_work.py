from __future__ import annotations
import abc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from leodb.core.engine import get_db_session
from leodb.models.general.account import Account
from leodb.models.general.user import User
from leodb.models.account.conversation import Conversation
from leodb.models.account.message import Message
from leodb.models.account.project import Project
from leodb.models.account.data_source import DataSource
from leodb.models.account.tool_use_spec import ToolUseSpec
from leodb.models.account.project_step import ProjectStep
from leodb.models.account.project_output import ProjectOutput
from leodb.models.account.record import Record
from leodb.models.general.user_session import UserSession
from leodb.models.general.user_preferences import UserPreferences
from leodb.models.general.user_invitation import UserInvitation
from leodb.models.general.invoice import Invoice
from leodb.models.general.package import Package
from leodb.models.general.payment_method import PaymentMethod

from leodb.repositories.user_repository import UserRepository
from leodb.repositories.account_repository import AccountRepository
from leodb.repositories.conversation_repository import ConversationRepository
from leodb.repositories.message_repository import MessageRepository
from leodb.repositories.user_session_repository import UserSessionRepository
from leodb.repositories.user_preferences_repository import UserPreferencesRepository
from leodb.repositories.user_invitation_repository import UserInvitationRepository
from leodb.repositories.invoice_repository import InvoiceRepository
from leodb.repositories.package_repository import PackageRepository
from leodb.repositories.payment_method_repository import PaymentMethodRepository
from leodb.repositories.project_repository import ProjectRepository
from leodb.repositories.datasource_repository import DataSourceRepository
from leodb.repositories.tool_use_spec_repository import ToolUseSpecRepository
from leodb.repositories.project_step_repository import ProjectStepRepository
from leodb.repositories.project_output_repository import ProjectOutputRepository
from leodb.repositories.record_repository import RecordRepository
# Import other repositories here as they are created

class AbstractUnitOfWork(abc.ABC):
    users: UserRepository
    accounts: AccountRepository
    conversations: ConversationRepository
    messages: MessageRepository
    sessions: UserSessionRepository
    preferences: UserPreferencesRepository
    invitations: UserInvitationRepository
    invoices: InvoiceRepository
    packages: PackageRepository
    payment_methods: PaymentMethodRepository
    projects: ProjectRepository
    data_sources: DataSourceRepository
    tool_use_specs: ToolUseSpecRepository
    project_steps: ProjectStepRepository
    project_outputs: ProjectOutputRepository
    records: RecordRepository
    # Define other repositories here

    def __init__(self, account_uuid: Optional[str] = None):
        self.account_uuid = account_uuid
        self._session_context = get_db_session(account_uuid)

    async def __aenter__(self) -> AbstractUnitOfWork:
        self._session = await self._session_context.__aenter__()
        self.users = UserRepository(self._session, User)
        self.accounts = AccountRepository(self._session, Account)
        self.conversations = ConversationRepository(self._session, Conversation)
        self.messages = MessageRepository(self._session, Message)
        self.sessions = UserSessionRepository(self._session, UserSession)
        self.preferences = UserPreferencesRepository(self._session, UserPreferences)
        self.invitations = UserInvitationRepository(self._session, UserInvitation)
        self.invoices = InvoiceRepository(self._session, Invoice)
        self.packages = PackageRepository(self._session, Package)
        self.payment_methods = PaymentMethodRepository(self._session, PaymentMethod)
        self.projects = ProjectRepository(self._session, Project)
        self.data_sources = DataSourceRepository(self._session, DataSource)
        self.tool_use_specs = ToolUseSpecRepository(self._session, ToolUseSpec)
        self.project_steps = ProjectStepRepository(self._session, ProjectStep)
        self.project_outputs = ProjectOutputRepository(self._session, ProjectOutput)
        self.records = RecordRepository(self._session, Record)
        # Instantiate other repositories here
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # The session is automatically closed by the context manager from get_db_session
        if self._session:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        
        await self._session_context.__aexit__(exc_type, exc_val, exc_tb)


    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError

class UnitOfWork(AbstractUnitOfWork):

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()