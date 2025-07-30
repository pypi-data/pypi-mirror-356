# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["PatientRequestDocumentsParams"]


class PatientRequestDocumentsParams(TypedDict, total=False):
    mime_types: Annotated[List[str], PropertyInfo(alias="mimeTypes")]
    """The mime types of the documents to get. Defaults to application/pdf."""
