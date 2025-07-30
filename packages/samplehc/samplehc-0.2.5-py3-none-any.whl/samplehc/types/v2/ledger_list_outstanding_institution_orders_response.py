# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["LedgerListOutstandingInstitutionOrdersResponse", "Order"]


class Order(BaseModel):
    balance_usd_cents: float = FieldInfo(alias="balanceUsdCents")
    """The outstanding balance for the order in cents."""

    path: str
    """The ledger account path for the order."""

    type: str
    """The type of the ledger account."""

    name: Optional[str] = None
    """The name of the ledger account."""


class LedgerListOutstandingInstitutionOrdersResponse(BaseModel):
    orders: List[Order]
    """List of outstanding orders for the institution."""
