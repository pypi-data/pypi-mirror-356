from sqlalchemy.orm import declarative_base, DeclarativeBase
from sqlalchemy import MetaData
from leodb.core.config import settings

# Métadonnées centralisées avec le schéma par défaut
# Toutes les tables qui héritent de Base utiliseront ce schéma
metadata_obj = MetaData(schema=settings.POSTGRES_GENERAL_SCHEMA)

class Base(DeclarativeBase):
    """
    Classe de base pour tous les modèles SQLAlchemy.
    Applique un schéma par défaut à toutes les tables.
    """
    metadata = metadata_obj