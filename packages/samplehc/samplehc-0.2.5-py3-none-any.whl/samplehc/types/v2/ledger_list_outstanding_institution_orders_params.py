# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["LedgerListOutstandingInstitutionOrdersParams"]


class LedgerListOutstandingInstitutionOrdersParams(TypedDict, total=False):
    institution_id: Required[Annotated[str, PropertyInfo(alias="institutionId")]]
    """Identifier of the institution for which to retrieve outstanding orders."""
