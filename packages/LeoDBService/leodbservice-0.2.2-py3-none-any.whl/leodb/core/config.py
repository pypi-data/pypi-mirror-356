from pydantic_settings import BaseSettings
from pydantic import Field, computed_field
from dotenv import load_dotenv
from typing import Optional

# Charger les variables d'environnement depuis un fichier .env
# C'est utile pour le développement local.
load_dotenv()

class Settings(BaseSettings):
    """
    Configuration de la bibliothèque leodb.
    Lit les variables d'environnement.
    """
    # Configuration de la base de données
    POSTGRES_USER: str = Field(default="user")
    POSTGRES_PASSWORD: str = Field(default="password")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DATABASE: str = Field(default="leodb")
    POSTGRES_SSL_MODE: Optional[str] = Field(default=None) # Ex: require, prefer, allow

    # Configuration des schémas
    POSTGRES_GENERAL_SCHEMA: str = Field(default="general")
    POSTGRES_ACCOUNT_SCHEMA_PREFIX: str = Field(default="acct_")

    # Limites de conservation des données
    POSTGRES_MAX_MESSAGES_PER_CONVERSATION: int = Field(default=100)
    POSTGRES_MAX_CONVERSATION_AGE_DAYS: int = Field(default=30)

    # Configuration Azure Key Vault pour le chiffrement
    AZURE_KEY_VAULT_URL: Optional[str] = Field(default=None)
    ENCRYPTION_KEY_NAME: Optional[str] = Field(default=None)
    
    # Clé de secours si Key Vault n'est pas disponible
    SECRET_KEY: str = Field(default="a_very_secret_key_that_should_be_changed")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Construit et retourne l'URL de connexion à la base de données."""
        url = (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"
        )
        if self.POSTGRES_SSL_MODE:
            url += f"?sslmode={self.POSTGRES_SSL_MODE}"
        return url

    @computed_field
    @property
    def is_azure_key_vault_enabled(self) -> bool:
        """Vérifie si la configuration pour Azure Key Vault est présente."""
        return bool(self.AZURE_KEY_VAULT_URL and self.ENCRYPTION_KEY_NAME)

# Instance globale des configurations
settings = Settings()