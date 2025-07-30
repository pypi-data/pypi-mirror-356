from sqlalchemy import text
from leodb.core.connection_manager import connection_manager
from leodb.models.account_base import account_metadata
from leodb.core.config import settings

async def provision_account_schema(account_uuid: str):
    """
    Creates a new schema for an account and deploys all account-specific tables into it.

    This function is idempotent. If the schema or tables already exist, it will
    not raise an error.

    The schema name is automatically generated based on the POSTGRES_ACCOUNT_SCHEMA_PREFIX
    setting and the account_uuid.

    Args:
        account_uuid: The UUID of the account for which to create the schema.
    """
    schema_name = f"{settings.POSTGRES_ACCOUNT_SCHEMA_PREFIX}{account_uuid}".replace("-", "_")
    # Get the specific engine for the target account's database
    engine = await connection_manager.get_engine(account_uuid)

    async with engine.begin() as conn:
        # Create the schema if it doesn't exist
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS \"{schema_name}\""))

        # Deploy only the tables associated with account_metadata into the new schema
        # We must specify the schema in the create_all call.
        for table in account_metadata.sorted_tables:
            table.schema = schema_name
        
        await conn.run_sync(account_metadata.create_all, checkfirst=True)

        # Reset the schema on the metadata tables to None so it doesn't affect
        # other operations that might use the same metadata object in the application's lifecycle.
        for table in account_metadata.sorted_tables:
            table.schema = None