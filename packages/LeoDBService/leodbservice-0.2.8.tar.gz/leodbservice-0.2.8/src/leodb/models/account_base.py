from sqlalchemy import MetaData

# Specific metadata for account-related tables.
# This allows us to create all account tables in a specific schema
# without affecting the 'general' tables.
account_metadata = MetaData()