from typing import Optional
from fastapi import Depends, Header

from leodb.services.unit_of_work import UnitOfWork


def get_current_account_id(x_account_id: Optional[str] = Header(None)) -> Optional[str]:
    """
    FastAPI dependency to extract the account ID from the 'X-Account-ID' header.
    
    This makes the account context explicit for each request.
    """
    return x_account_id


def get_uow(
    account_id: Optional[str] = Depends(get_current_account_id),
) -> UnitOfWork:
    """
    FastAPI dependency that provides a UnitOfWork instance tailored for the request.

    It will be configured with both a general session and an account-specific
    session if an 'X-Account-ID' is provided.
    """
    return UnitOfWork(account_uuid=account_id)