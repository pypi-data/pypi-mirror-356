"""Fillbert document processing Python client library."""

from .client import FillbertClient
from .models import (
    DocumentResult,
    JobStatus,
    ProcessingJob,
    ExtractedData,
    ProcessingMetrics,
    JobStatusEnum,
)

# FastAPI webhook support (optional)
try:
    from .webhook import (  # noqa: F401
        create_webhook_router,
        create_simple_webhook_router,
        WebhookPayload,
        verify_webhook_signature,
    )

    _webhook_exports = [
        "create_webhook_router",
        "create_simple_webhook_router",
        "WebhookPayload",
        "verify_webhook_signature",
    ]
except ImportError:
    # FastAPI not installed
    _webhook_exports = []

__version__ = "0.1.0"
__all__ = [
    "FillbertClient",
    "DocumentResult",
    "JobStatus",
    "ProcessingJob",
    "ExtractedData",
    "ProcessingMetrics",
    "JobStatusEnum",
] + _webhook_exports
