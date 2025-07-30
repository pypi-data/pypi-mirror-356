"""Fillbert document processing client implementation."""

import httpx

from .models import DocumentResult, JobStatus, ProcessingJob


class FillbertClient:
    """Client for Fillbert document processing service."""

    def __init__(self, base_url: str, api_key: str) -> None:
        """Initialize Fillbert client.

        Args:
            base_url: Base URL of the Fillbert processing service
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0,
        )

    async def process_document(
        self,
        document_path: str,
        callback_url: str | None = None,
        webhook_secret: str | None = None,
    ) -> ProcessingJob:
        """Submit document for processing.

        Args:
            document_path: Path to document file to upload
            callback_url: Optional webhook URL for completion notification
            webhook_secret: Optional secret for webhook validation

        Returns:
            ProcessingJob with request_id and status
        """
        # Prepare form data
        form_data = {}
        if callback_url:
            form_data["callback_url"] = callback_url
        if webhook_secret:
            form_data["webhook_secret"] = webhook_secret

        # Open and upload file
        with open(document_path, "rb") as f:
            files = {"document": f}
            response = await self._client.post(
                f"{self.base_url}/api/v1/process",
                data=form_data,
                files=files,
            )
            response.raise_for_status()

        data = response.json()
        return ProcessingJob(
            request_id=data["request_id"],
            status=data["status"],
            message=data.get("message", ""),
        )

    async def get_job_status(self, request_id: str) -> JobStatus:
        """Get current job status.

        Args:
            request_id: Job request ID

        Returns:
            Current job status
        """
        response = await self._client.get(f"{self.base_url}/api/v1/jobs/{request_id}")
        response.raise_for_status()
        data = response.json()

        return JobStatus(
            request_id=data["request_id"],
            status=data["status"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            error_message=data.get("error_message"),
            retry_count=data.get("retry_count", 0),
            webhook_delivered=data.get("webhook_delivered", False),
        )

    async def get_result(self, request_id: str) -> DocumentResult:
        """Get extracted document data.

        Args:
            request_id: Job request ID

        Returns:
            Extracted document data
        """
        response = await self._client.get(
            f"{self.base_url}/api/v1/jobs/{request_id}/result"
        )
        response.raise_for_status()
        data = response.json()

        return DocumentResult(
            request_id=data["request_id"],
            status=data["status"],
            extracted_data=data.get("extracted_data"),
            metrics=data.get("metrics"),
            error_message=data.get("error_message"),
        )

    async def wait_for_completion(
        self, request_id: str, poll_interval: float = 2.0, timeout: float = 300.0
    ) -> DocumentResult:
        """Wait for job completion and return result.

        Args:
            request_id: Job request ID
            poll_interval: Seconds between status checks
            timeout: Maximum time to wait in seconds

        Returns:
            Extracted document data

        Raises:
            TimeoutError: If job doesn't complete within timeout
            RuntimeError: If job fails
        """
        import asyncio
        import time

        start_time = time.time()

        while time.time() - start_time < timeout:
            status = await self.get_job_status(request_id)

            if status.status in ["completed"]:
                return await self.get_result(request_id)
            elif status.status in ["failed", "cancelled"]:
                raise RuntimeError(f"Job failed: {status.error_message}")

            await asyncio.sleep(poll_interval)

        raise TimeoutError(
            f"Job {request_id} did not complete within {timeout} seconds"
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
