"""Fillbert document processing client data models."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class JobStatusEnum(str, Enum):
    """Job processing status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProcessingJob(BaseModel):
    """Document processing job submission response."""

    request_id: str
    status: JobStatusEnum
    message: str


class JobStatus(BaseModel):
    """Current job status."""

    request_id: str
    status: JobStatusEnum
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    retry_count: int = 0
    webhook_delivered: bool = False


class ProcessingMetrics(BaseModel):
    """Processing performance metrics."""

    ai_provider: str
    model_used: str
    processing_time_seconds: float
    tokens_used: int | None = None
    cost_usd: float | None = None
    confidence_score: float | None = None


class ExtractedData(BaseModel):
    """Extracted document data structure."""

    document_number: str | None = None
    date: str | None = None
    carrier: str | None = None
    driver: str | None = None
    products: list[dict[str, Any]] = []
    quantities: dict[str, Any] = {}
    locations: dict[str, str] = {}
    raw_text: str | None = None
    confidence_score: float | None = None


class DocumentResult(BaseModel):
    """Extracted document data result."""

    request_id: str
    status: JobStatusEnum
    extracted_data: ExtractedData | None = None
    metrics: ProcessingMetrics | None = None
    error_message: str | None = None
