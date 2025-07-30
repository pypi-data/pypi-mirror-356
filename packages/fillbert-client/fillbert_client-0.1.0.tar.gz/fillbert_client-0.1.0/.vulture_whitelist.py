# Vulture whitelist for Fillbert Client Library

# Client API methods (public interface)
FillbertClient
process_document
get_job_status
get_result
wait_for_completion
close

# Status enum values (used by API consumers)
PENDING
PROCESSING
COMPLETED
FAILED
CANCELLED

# Model fields (used by Pydantic serialization)
message
status
created_at
updated_at
started_at
completed_at
error_message
retry_count
webhook_delivered
extracted_data
metrics
confidence_scores
processing_time_ms
model_used
ai_provider
processing_time_seconds
tokens_used
cost_usd
confidence_score
document_number
date
carrier
driver
products
quantities
locations
raw_text

# Webhook module public API (FastAPI integration)
handle_fillbert_webhook
x_fillbert_request_id
x_fillbert_timestamp
create_simple_webhook_router
