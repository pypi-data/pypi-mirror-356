# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["PatientRequestDocumentsResponse"]


class PatientRequestDocumentsResponse(BaseModel):
    async_result_id: str = FieldInfo(alias="asyncResultId")
    """The async result ID.

    When the async result completes, the result will contain an array of document
    objects, each with id, fileName, and mimeType.
    """
