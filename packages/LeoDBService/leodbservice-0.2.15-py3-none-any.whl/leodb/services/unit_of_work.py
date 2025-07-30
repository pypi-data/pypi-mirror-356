from __future__ import annotations
import abc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

# Importez le connection_manager global au lieu de get_db_session
from leodb.core.connection_manager import connection_manager

# --- Imports des Models (inchangés) ---
from leodb.models.general.account import Account
from leodb.models.general.user import User
from leodb.models.general.user_session import UserSession
from leodb.models.general.user_preferences import UserPreferences
from leodb.models.general.user_invitation import UserInvitation
from leodb.models.general.invoice import Invoice
from leodb.models.general.package import Package
from leodb.models.general.payment_method import PaymentMethod
from leodb.models.account.conversation import Conversation
from leodb.models.account.message import Message
from leodb.models.account.project import Project
from leodb.models.account.data_source import DataSource
from leodb.models.account.tool_use_spec import ToolUseSpec
from leodb.models.account.project_step import ProjectStep
from leodb.models.account.project_output import ProjectOutput
from leodb.models.account.record import Record

# --- Imports des Repositories (inchangés) ---
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


class AbstractUnitOfWork(abc.ABC):
    # Repositories généraux
    users: UserRepository
    accounts: AccountRepository
    sessions: UserSessionRepository
    preferences: UserPreferencesRepository
    invitations: UserInvitationRepository
    invoices: InvoiceRepository
    packages: PackageRepository
    payment_methods: PaymentMethodRepository

    # Repositories de compte (peuvent être None)
    conversations: Optional[ConversationRepository]
    messages: Optional[MessageRepository]
    projects: Optional[ProjectRepository]
    data_sources: Optional[DataSourceRepository]
    tool_use_specs: Optional[ToolUseSpecRepository]
    project_steps: Optional[ProjectStepRepository]
    project_outputs: Optional[ProjectOutputRepository]
    records: Optional[RecordRepository]

    def __init__(self, account_uuid: Optional[str] = None):
        self.account_uuid = account_uuid
        self._general_session: Optional[AsyncSession] = None
        self._account_session: Optional[AsyncSession] = None

    async def __aenter__(self) -> AbstractUnitOfWork:
        # 1. Obtenir la session générale (toujours)
        self._general_session = await connection_manager.get_session()

        # 2. Obtenir la session de compte (seulement si un UUID est fourni)
        if self.account_uuid:
            self._account_session = await connection_manager.get_session(self.account_uuid)
        
        # 3. Instancier les repositories avec la bonne session
        # Repositories généraux
        self.users = UserRepository(self._general_session, User)
        self.accounts = AccountRepository(self._general_session, Account)
        self.sessions = UserSessionRepository(self._general_session, UserSession)
        self.preferences = UserPreferencesRepository(self._general_session, UserPreferences)
        self.invitations = UserInvitationRepository(self._general_session, UserInvitation)
        self.invoices = InvoiceRepository(self._general_session, Invoice)
        self.packages = PackageRepository(self._general_session, Package)
        self.payment_methods = PaymentMethodRepository(self._general_session, PaymentMethod)

        # Repositories de compte
        if self._account_session:
            self.conversations = ConversationRepository(self._account_session, Conversation)
            self.messages = MessageRepository(self._account_session, Message)
            self.projects = ProjectRepository(self._account_session, Project)
            self.data_sources = DataSourceRepository(self._account_session, DataSource)
            self.tool_use_specs = ToolUseSpecRepository(self._account_session, ToolUseSpec)
            self.project_steps = ProjectStepRepository(self._account_session, ProjectStep)
            self.project_outputs = ProjectOutputRepository(self._account_session, ProjectOutput)
            self.records = RecordRepository(self._account_session, Record)
        else:
            # S'il n'y a pas de session de compte, les repositories associés sont None
            self.conversations = None
            self.messages = None
            self.projects = None
            self.data_sources = None
            self.tool_use_specs = None
            self.project_steps = None
            self.project_outputs = None
            self.records = None

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Fermer les sessions dans un bloc finally pour garantir leur fermeture
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            if self._general_session:
                await self._general_session.close()
            if self._account_session:
                await self._account_session.close()

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError

class UnitOfWork(AbstractUnitOfWork):

    async def commit(self):
        # Commiter les deux sessions.
        # ATTENTION: Ce n'est pas une transaction atomique distribuée (2PC).
        # Si le premier commit réussit et le second échoue, les données peuvent être incohérentes.
        # Pour de nombreuses applications, c'est un compromis acceptable.
        if self._account_session:
            await self._account_session.commit()
        if self._general_session:
            await self._general_session.commit()

    async def rollback(self):
        # Annuler les deux transactions
        if self._account_session:
            await self._account_session.rollback()
        if self._general_session:
            await self._general_session.rollback()