# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.v2.hie import patient_request_documents_params, patient_request_fhir_data_params
from ....types.v2.hie.patient_request_documents_response import PatientRequestDocumentsResponse
from ....types.v2.hie.patient_request_fhir_data_response import PatientRequestFhirDataResponse

__all__ = ["PatientResource", "AsyncPatientResource"]


class PatientResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PatientResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return PatientResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PatientResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return PatientResourceWithStreamingResponse(self)

    def request_documents(
        self,
        patient_id: str,
        *,
        mime_types: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PatientRequestDocumentsResponse:
        """
        Triggers a job to get patient documents of specific mime types from HIE.

        Args:
          mime_types: The mime types of the documents to get. Defaults to application/pdf.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not patient_id:
            raise ValueError(f"Expected a non-empty value for `patient_id` but received {patient_id!r}")
        return self._post(
            f"/api/v2/hie/patient/{patient_id}/documents",
            body=maybe_transform(
                {"mime_types": mime_types}, patient_request_documents_params.PatientRequestDocumentsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PatientRequestDocumentsResponse,
        )

    def request_fhir_data(
        self,
        patient_id: str,
        *,
        resource_types: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PatientRequestFhirDataResponse:
        """
        Triggers a job to get a FHIR bundle for a patient from HIE.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not patient_id:
            raise ValueError(f"Expected a non-empty value for `patient_id` but received {patient_id!r}")
        return self._post(
            f"/api/v2/hie/patient/{patient_id}/fhir",
            body=maybe_transform(
                {"resource_types": resource_types}, patient_request_fhir_data_params.PatientRequestFhirDataParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PatientRequestFhirDataResponse,
        )


class AsyncPatientResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPatientResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPatientResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPatientResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return AsyncPatientResourceWithStreamingResponse(self)

    async def request_documents(
        self,
        patient_id: str,
        *,
        mime_types: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PatientRequestDocumentsResponse:
        """
        Triggers a job to get patient documents of specific mime types from HIE.

        Args:
          mime_types: The mime types of the documents to get. Defaults to application/pdf.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not patient_id:
            raise ValueError(f"Expected a non-empty value for `patient_id` but received {patient_id!r}")
        return await self._post(
            f"/api/v2/hie/patient/{patient_id}/documents",
            body=await async_maybe_transform(
                {"mime_types": mime_types}, patient_request_documents_params.PatientRequestDocumentsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PatientRequestDocumentsResponse,
        )

    async def request_fhir_data(
        self,
        patient_id: str,
        *,
        resource_types: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PatientRequestFhirDataResponse:
        """
        Triggers a job to get a FHIR bundle for a patient from HIE.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not patient_id:
            raise ValueError(f"Expected a non-empty value for `patient_id` but received {patient_id!r}")
        return await self._post(
            f"/api/v2/hie/patient/{patient_id}/fhir",
            body=await async_maybe_transform(
                {"resource_types": resource_types}, patient_request_fhir_data_params.PatientRequestFhirDataParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PatientRequestFhirDataResponse,
        )


class PatientResourceWithRawResponse:
    def __init__(self, patient: PatientResource) -> None:
        self._patient = patient

        self.request_documents = to_raw_response_wrapper(
            patient.request_documents,
        )
        self.request_fhir_data = to_raw_response_wrapper(
            patient.request_fhir_data,
        )


class AsyncPatientResourceWithRawResponse:
    def __init__(self, patient: AsyncPatientResource) -> None:
        self._patient = patient

        self.request_documents = async_to_raw_response_wrapper(
            patient.request_documents,
        )
        self.request_fhir_data = async_to_raw_response_wrapper(
            patient.request_fhir_data,
        )


class PatientResourceWithStreamingResponse:
    def __init__(self, patient: PatientResource) -> None:
        self._patient = patient

        self.request_documents = to_streamed_response_wrapper(
            patient.request_documents,
        )
        self.request_fhir_data = to_streamed_response_wrapper(
            patient.request_fhir_data,
        )


class AsyncPatientResourceWithStreamingResponse:
    def __init__(self, patient: AsyncPatientResource) -> None:
        self._patient = patient

        self.request_documents = async_to_streamed_response_wrapper(
            patient.request_documents,
        )
        self.request_fhir_data = async_to_streamed_response_wrapper(
            patient.request_fhir_data,
        )
