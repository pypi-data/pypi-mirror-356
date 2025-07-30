"""Test the Fillbert client."""

import pytest
import respx
import httpx
from unittest.mock import patch, mock_open
from fillbert_client import (
    FillbertClient,
    ProcessingJob,
    JobStatus,
    DocumentResult,
    JobStatusEnum,
)


def test_client_init() -> None:
    """Test client initialization."""
    client = FillbertClient(base_url="https://api.example.com/", api_key="test-key")

    assert client.base_url == "https://api.example.com"
    assert client.api_key == "test-key"


@pytest.mark.asyncio
@respx.mock
async def test_process_document_success() -> None:
    """Test successful document processing submission."""
    # Mock file reading
    mock_file_content = b"fake PDF content"

    # Mock API response
    respx.post("https://api.example.com/api/v1/process").mock(
        return_value=httpx.Response(
            200,
            json={
                "request_id": "req_123456789_abcd",
                "status": "pending",
                "message": "document submitted for processing",
            },
        )
    )

    client = FillbertClient(base_url="https://api.example.com", api_key="test-key")

    # More specific mock that doesn't interfere with mimetypes
    mock_file = mock_open(read_data=mock_file_content)
    with patch("fillbert_client.client.open", mock_file):
        job = await client.process_document(
            document_path="test.pdf",
            callback_url="https://example.com/webhook",
            webhook_secret="secret123",
        )

    assert isinstance(job, ProcessingJob)
    assert job.request_id == "req_123456789_abcd"
    assert job.status == JobStatusEnum.PENDING
    assert job.message == "document submitted for processing"


@pytest.mark.asyncio
@respx.mock
async def test_get_job_status() -> None:
    """Test getting job status."""
    respx.get("https://api.example.com/api/v1/jobs/req_123").mock(
        return_value=httpx.Response(
            200,
            json={
                "request_id": "req_123",
                "status": "processing",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:01:00Z",
                "started_at": "2023-01-01T00:01:00Z",
                "completed_at": None,
                "error_message": None,
                "retry_count": 0,
                "webhook_delivered": False,
            },
        )
    )

    client = FillbertClient(base_url="https://api.example.com", api_key="test-key")
    status = await client.get_job_status("req_123")

    assert isinstance(status, JobStatus)
    assert status.request_id == "req_123"
    assert status.status == JobStatusEnum.PROCESSING
    assert status.retry_count == 0
    assert status.webhook_delivered is False


@pytest.mark.asyncio
@respx.mock
async def test_get_result() -> None:
    """Test getting job result."""
    respx.get("https://api.example.com/api/v1/jobs/req_123/result").mock(
        return_value=httpx.Response(
            200,
            json={
                "request_id": "req_123",
                "status": "completed",
                "extracted_data": {
                    "document_number": "document123456",
                    "carrier": "ACME Transport",
                    "date": "2023-01-01",
                },
                "metrics": {
                    "ai_provider": "anthropic",
                    "model_used": "claude-3.5-sonnet",
                    "processing_time_seconds": 1.5,
                    "cost_usd": 0.05,
                },
                "error_message": None,
            },
        )
    )

    client = FillbertClient(base_url="https://api.example.com", api_key="test-key")
    result = await client.get_result("req_123")

    assert isinstance(result, DocumentResult)
    assert result.request_id == "req_123"
    assert result.status == JobStatusEnum.COMPLETED
    assert result.extracted_data is not None
    assert result.extracted_data.document_number == "document123456"
    assert result.extracted_data.carrier == "ACME Transport"
    assert result.metrics is not None
    assert result.metrics.ai_provider == "anthropic"
    assert result.metrics.cost_usd == 0.05


@pytest.mark.asyncio
@respx.mock
async def test_wait_for_completion_success() -> None:
    """Test waiting for job completion."""
    # Mock status calls - first processing, then completed
    respx.get("https://api.example.com/api/v1/jobs/req_123").mock(
        side_effect=[
            httpx.Response(
                200,
                json={
                    "request_id": "req_123",
                    "status": "processing",
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-01T00:01:00Z",
                },
            ),
            httpx.Response(
                200,
                json={
                    "request_id": "req_123",
                    "status": "completed",
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-01T00:02:00Z",
                },
            ),
        ]
    )

    # Mock result call
    respx.get("https://api.example.com/api/v1/jobs/req_123/result").mock(
        return_value=httpx.Response(
            200,
            json={
                "request_id": "req_123",
                "status": "completed",
                "extracted_data": {"document_number": "document123"},
                "metrics": None,
                "error_message": None,
            },
        )
    )

    client = FillbertClient(base_url="https://api.example.com", api_key="test-key")
    result = await client.wait_for_completion("req_123", poll_interval=0.1)

    assert result.request_id == "req_123"
    assert result.extracted_data is not None
    assert result.extracted_data.document_number == "document123"


@pytest.mark.asyncio
@respx.mock
async def test_wait_for_completion_failure() -> None:
    """Test waiting for job that fails."""
    respx.get("https://api.example.com/api/v1/jobs/req_123").mock(
        return_value=httpx.Response(
            200,
            json={
                "request_id": "req_123",
                "status": "failed",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:01:00Z",
                "error_message": "Processing failed",
            },
        )
    )

    client = FillbertClient(base_url="https://api.example.com", api_key="test-key")

    with pytest.raises(RuntimeError, match="Job failed: Processing failed"):
        await client.wait_for_completion("req_123")


@pytest.mark.asyncio
async def test_close() -> None:
    """Test client cleanup."""
    client = FillbertClient(base_url="https://api.example.com", api_key="test-key")
    await client.close()  # Should not raise
