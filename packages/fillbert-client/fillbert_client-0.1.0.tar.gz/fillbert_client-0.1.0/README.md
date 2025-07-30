# Fillbert Client

Python client library for the Fillbert document processing service.

## Installation

```bash
# Basic installation
pip install fillbert-client

# With FastAPI webhook support
pip install fillbert-client[fastapi]
```

## Basic Usage

```python
import asyncio
from fillbert_client import FillbertClient

async def main():
    # Initialize client
    client = FillbertClient(
        base_url="https://bol-ocr.example.com",
        api_key="your-api-key"
    )

    try:
        # Process document with optional webhook
        job = await client.process_document(
            image_path="path/to/document.pdf",
            callback_url="https://your-app.com/webhooks/bol-complete",
            webhook_secret="your-webhook-secret"
        )

        print(f"Job submitted: {job.request_id}")

        # Option 1: Poll for completion
        result = await client.wait_for_completion(job.request_id)
        print(f"Processing completed: {result.extracted_data}")

        # Option 2: Check status manually
        status = await client.get_job_status(job.request_id)
        if status.status == "completed":
            result = await client.get_result(job.request_id)
            print(f"document Number: {result.extracted_data.bol_number}")
            print(f"Carrier: {result.extracted_data.carrier}")

    finally:
        await client.close()

# Run async function
asyncio.run(main())
```

## Webhook Integration (FastAPI)

If you're using FastAPI, you can automatically handle webhooks:

```python
from fastapi import FastAPI
from fillbert_client import create_simple_webhook_router, JobStatusEnum

app = FastAPI()

def handle_completion(payload):
    print(f"document {payload.request_id} completed!")
    print(f"Extracted data: {payload.extracted_data}")
    # Store in database, send notifications, etc.

def handle_failure(payload):
    print(f"document {payload.request_id} failed: {payload.error_message}")
    # Handle error, retry, notify user, etc.

# Create webhook router
webhook_router = create_simple_webhook_router(
    secret="your-webhook-secret",
    on_completion=handle_completion,
    on_failure=handle_failure,
)

# Mount webhook endpoints at /webhooks/bol-complete
app.include_router(webhook_router)

# Your webhook URL will be: https://your-app.com/webhooks/bol-complete
```

## Advanced Webhook Handling

For more control over webhook handling:

```python
from fastapi import FastAPI
from fillbert_client import create_webhook_router, JobStatusEnum

def handle_processing(payload):
    print(f"document {payload.request_id} is now processing...")

def handle_completion(payload):
    print(f"document {payload.request_id} completed!")

def handle_failure(payload):
    print(f"document {payload.request_id} failed!")

app = FastAPI()

webhook_router = create_webhook_router(
    secret="your-webhook-secret",
    path_prefix="/api/webhooks",  # Custom prefix
    endpoint_name="bol-events",   # Custom endpoint name
    handlers={
        JobStatusEnum.PROCESSING: handle_processing,
        JobStatusEnum.COMPLETED: handle_completion,
        JobStatusEnum.FAILED: handle_failure,
    }
)

app.include_router(webhook_router)
# Webhook URL: https://your-app.com/api/webhooks/bol-events
```

## Error Handling

```python
from fillbert_client import FillbertClient
import httpx

async def process_with_error_handling():
    client = FillbertClient(base_url="...", api_key="...")

    try:
        job = await client.process_document("document.pdf")
        result = await client.wait_for_completion(
            job.request_id,
            timeout=300  # 5 minutes
        )
        return result

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            print("Callback URL not authorized for this client")
        elif e.response.status_code == 400:
            print("Invalid request - check file format and parameters")
        else:
            print(f"HTTP error: {e}")

    except TimeoutError:
        print("document processing timed out")

    except RuntimeError as e:
        print(f"Processing failed: {e}")

    finally:
        await client.close()
```

## Development

This package is part of the document OCR Service monorepo.

```bash
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest

# Run tests with auto-watcher
uv run ptw

# Run quality checks
uv run ruff check .
uv run mypy .
```
