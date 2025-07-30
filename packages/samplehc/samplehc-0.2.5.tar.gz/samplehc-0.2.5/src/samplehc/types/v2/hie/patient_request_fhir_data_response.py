# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["PatientRequestFhirDataResponse"]


class PatientRequestFhirDataResponse(BaseModel):
    async_result_id: str = FieldInfo(alias="asyncResultId")
    """The async result ID.

    When the async result completes, the result will contain a document object with
    id, fileName, and mimeType fields representing the FHIR JSON file.
    """
