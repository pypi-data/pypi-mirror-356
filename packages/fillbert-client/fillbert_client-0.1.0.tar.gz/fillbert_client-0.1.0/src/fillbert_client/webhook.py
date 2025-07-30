"""FastAPI webhook router factory for Fillbert document processing client."""

import hashlib
import hmac
import json
from typing import Any, Callable, Dict, Optional

from fastapi import APIRouter, HTTPException, Request, Header
from pydantic import BaseModel

from .models import JobStatusEnum


class WebhookPayload(BaseModel):
    """Webhook payload structure."""

    request_id: str
    status: JobStatusEnum
    created_at: str
    updated_at: str
    started_at: str | None = None
    completed_at: str | None = None
    extracted_data: Dict[str, Any] | None = None
    metrics: Dict[str, Any] | None = None
    error_message: str | None = None
    retry_count: int | None = None


def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    """Verify webhook HMAC signature.

    Args:
        payload: Raw webhook payload string
        signature: Signature from X-Fillbert-Signature header
        secret: Webhook secret for verification

    Returns:
        True if signature is valid, False otherwise
    """
    if not signature.startswith("sha256="):
        return False

    expected_signature = hmac.new(
        secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature[7:], expected_signature)


def create_webhook_router(
    secret: str,
    path_prefix: str = "/webhooks",
    endpoint_name: str = "bol-complete",
    handlers: Optional[Dict[JobStatusEnum, Callable[[WebhookPayload], Any]]] = None,
) -> APIRouter:
    """Create a FastAPI router for document webhook handling.

    Args:
        secret: Webhook secret for signature verification
        path_prefix: URL path prefix for webhook endpoints
        endpoint_name: Name of the webhook endpoint
        handlers: Optional dict mapping job statuses to handler functions

    Returns:
        FastAPI router with webhook endpoint

    Example:
        ```python
        from fastapi import FastAPI
        from bol_ocr_client import create_webhook_router, JobStatusEnum

        def handle_completion(payload):
            print(f"Job {payload.request_id} completed!")
            if payload.extracted_data:
                print(f"Extracted data: {payload.extracted_data}")

        def handle_failure(payload):
            print(f"Job {payload.request_id} failed: {payload.error_message}")

        app = FastAPI()

        webhook_router = create_webhook_router(
            secret="your-webhook-secret",
            handlers={
                JobStatusEnum.COMPLETED: handle_completion,
                JobStatusEnum.FAILED: handle_failure,
            }
        )

        app.include_router(webhook_router)
        ```
    """
    router = APIRouter(prefix=path_prefix, tags=["webhooks"])

    @router.post(f"/{endpoint_name}")
    async def handle_fillbert_webhook(
        request: Request,
        x_fillbert_signature: Optional[str] = Header(
            None, alias="X-Fillbert-Signature"
        ),
        x_fillbert_request_id: Optional[str] = Header(
            None, alias="X-Fillbert-Request-ID"
        ),
        x_fillbert_timestamp: Optional[str] = Header(
            None, alias="X-Fillbert-Timestamp"
        ),
    ):
        """Handle document processing webhook."""
        # Read raw body for signature verification
        raw_body = await request.body()
        payload_str = raw_body.decode("utf-8")

        # Verify signature
        if x_fillbert_signature:
            if not verify_webhook_signature(payload_str, x_fillbert_signature, secret):
                raise HTTPException(status_code=401, detail="Invalid webhook signature")

        # Parse payload
        try:
            payload_data = json.loads(payload_str)
            payload = WebhookPayload(**payload_data)
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(status_code=400, detail=f"Invalid payload: {e}")

        # Call appropriate handler if provided
        if handlers and payload.status in handlers:
            try:
                await handlers[payload.status](payload)
            except Exception as e:
                # Log error but don't fail the webhook
                print(f"Error in webhook handler: {e}")

        return {"status": "ok", "request_id": payload.request_id}

    return router


# Convenience function for common use case
def create_simple_webhook_router(
    secret: str,
    on_completion: Optional[Callable[[WebhookPayload], Any]] = None,
    on_failure: Optional[Callable[[WebhookPayload], Any]] = None,
    path_prefix: str = "/webhooks",
) -> APIRouter:
    """Create a simple webhook router with completion and failure handlers.

    Args:
        secret: Webhook secret for signature verification
        on_completion: Handler function for completed jobs
        on_failure: Handler function for failed jobs
        path_prefix: URL path prefix for webhook endpoints

    Returns:
        FastAPI router with webhook endpoint

    Example:
        ```python
        from fastapi import FastAPI
        from bol_ocr_client import create_simple_webhook_router

        def handle_success(payload):
            print(f"document processing completed: {payload.request_id}")

        def handle_error(payload):
            print(f"document processing failed: {payload.error_message}")

        app = FastAPI()
        webhook_router = create_simple_webhook_router(
            secret="your-secret",
            on_completion=handle_success,
            on_failure=handle_error
        )
        app.include_router(webhook_router)
        ```
    """
    handlers = {}
    if on_completion:
        handlers[JobStatusEnum.COMPLETED] = on_completion
    if on_failure:
        handlers[JobStatusEnum.FAILED] = on_failure

    return create_webhook_router(
        secret=secret,
        path_prefix=path_prefix,
        handlers=handlers,
    )
