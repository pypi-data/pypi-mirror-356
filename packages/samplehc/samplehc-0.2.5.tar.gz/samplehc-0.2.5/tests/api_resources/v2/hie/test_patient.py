# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from samplehc import SampleHealthcare, AsyncSampleHealthcare
from tests.utils import assert_matches_type
from samplehc.types.v2.hie import (
    PatientRequestFhirDataResponse,
    PatientRequestDocumentsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPatient:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_request_documents(self, client: SampleHealthcare) -> None:
        patient = client.v2.hie.patient.request_documents(
            patient_id="patientId",
        )
        assert_matches_type(PatientRequestDocumentsResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_request_documents_with_all_params(self, client: SampleHealthcare) -> None:
        patient = client.v2.hie.patient.request_documents(
            patient_id="patientId",
            mime_types=["string"],
        )
        assert_matches_type(PatientRequestDocumentsResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_request_documents(self, client: SampleHealthcare) -> None:
        response = client.v2.hie.patient.with_raw_response.request_documents(
            patient_id="patientId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        patient = response.parse()
        assert_matches_type(PatientRequestDocumentsResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_request_documents(self, client: SampleHealthcare) -> None:
        with client.v2.hie.patient.with_streaming_response.request_documents(
            patient_id="patientId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            patient = response.parse()
            assert_matches_type(PatientRequestDocumentsResponse, patient, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_request_documents(self, client: SampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `patient_id` but received ''"):
            client.v2.hie.patient.with_raw_response.request_documents(
                patient_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_request_fhir_data(self, client: SampleHealthcare) -> None:
        patient = client.v2.hie.patient.request_fhir_data(
            patient_id="patientId",
        )
        assert_matches_type(PatientRequestFhirDataResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_request_fhir_data_with_all_params(self, client: SampleHealthcare) -> None:
        patient = client.v2.hie.patient.request_fhir_data(
            patient_id="patientId",
            resource_types=["string"],
        )
        assert_matches_type(PatientRequestFhirDataResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_request_fhir_data(self, client: SampleHealthcare) -> None:
        response = client.v2.hie.patient.with_raw_response.request_fhir_data(
            patient_id="patientId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        patient = response.parse()
        assert_matches_type(PatientRequestFhirDataResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_request_fhir_data(self, client: SampleHealthcare) -> None:
        with client.v2.hie.patient.with_streaming_response.request_fhir_data(
            patient_id="patientId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            patient = response.parse()
            assert_matches_type(PatientRequestFhirDataResponse, patient, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_request_fhir_data(self, client: SampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `patient_id` but received ''"):
            client.v2.hie.patient.with_raw_response.request_fhir_data(
                patient_id="",
            )


class TestAsyncPatient:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_request_documents(self, async_client: AsyncSampleHealthcare) -> None:
        patient = await async_client.v2.hie.patient.request_documents(
            patient_id="patientId",
        )
        assert_matches_type(PatientRequestDocumentsResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_request_documents_with_all_params(self, async_client: AsyncSampleHealthcare) -> None:
        patient = await async_client.v2.hie.patient.request_documents(
            patient_id="patientId",
            mime_types=["string"],
        )
        assert_matches_type(PatientRequestDocumentsResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_request_documents(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.v2.hie.patient.with_raw_response.request_documents(
            patient_id="patientId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        patient = await response.parse()
        assert_matches_type(PatientRequestDocumentsResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_request_documents(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.v2.hie.patient.with_streaming_response.request_documents(
            patient_id="patientId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            patient = await response.parse()
            assert_matches_type(PatientRequestDocumentsResponse, patient, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_request_documents(self, async_client: AsyncSampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `patient_id` but received ''"):
            await async_client.v2.hie.patient.with_raw_response.request_documents(
                patient_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_request_fhir_data(self, async_client: AsyncSampleHealthcare) -> None:
        patient = await async_client.v2.hie.patient.request_fhir_data(
            patient_id="patientId",
        )
        assert_matches_type(PatientRequestFhirDataResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_request_fhir_data_with_all_params(self, async_client: AsyncSampleHealthcare) -> None:
        patient = await async_client.v2.hie.patient.request_fhir_data(
            patient_id="patientId",
            resource_types=["string"],
        )
        assert_matches_type(PatientRequestFhirDataResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_request_fhir_data(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.v2.hie.patient.with_raw_response.request_fhir_data(
            patient_id="patientId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        patient = await response.parse()
        assert_matches_type(PatientRequestFhirDataResponse, patient, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_request_fhir_data(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.v2.hie.patient.with_streaming_response.request_fhir_data(
            patient_id="patientId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            patient = await response.parse()
            assert_matches_type(PatientRequestFhirDataResponse, patient, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_request_fhir_data(self, async_client: AsyncSampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `patient_id` but received ''"):
            await async_client.v2.hie.patient.with_raw_response.request_fhir_data(
                patient_id="",
            )
