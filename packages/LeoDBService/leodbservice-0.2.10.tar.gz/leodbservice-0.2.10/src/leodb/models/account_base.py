from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

# Specific metadata for account-related tables.
# This allows us to create all account tables in a specific schema
# without affecting the 'general' tables.
account_metadata = MetaData()

# A specific declarative base for all account-related models.
# Models inheriting from this base will automatically be part of account_metadata.
AccountBase = declarative_base(metadata=account_metadata)