# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["PatientRequestFhirDataParams"]


class PatientRequestFhirDataParams(TypedDict, total=False):
    resource_types: Annotated[List[str], PropertyInfo(alias="resourceTypes")]
