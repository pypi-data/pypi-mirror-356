import datetime
import logging
import uuid
from typing import Dict, Any, Optional, Set, Tuple
from enum import Enum

import wrapt
from revenium_middleware import client, run_async_in_thread, shutdown_event

# Azure OpenAI support imports
from .provider import Provider, detect_provider, get_provider_metadata, is_azure_provider
from .azure_model_resolver import resolve_azure_model_name
from .config import Config, SecurityConfig
from .exceptions import (
    ReveniumMiddlewareError, ValidationError, MeteringError,
    NetworkError, AuthenticationError, categorize_exception, handle_exception_safely
)

logger = logging.getLogger("revenium_middleware.extension")


# Use centralized security configuration
SENSITIVE_FIELDS = SecurityConfig.SENSITIVE_FIELDS


def sanitize_for_logging(data: Any, max_depth: int = Config.MAX_SANITIZATION_DEPTH) -> Any:
    """
    Sanitize data for secure logging by redacting sensitive fields.

    Args:
        data: Data to sanitize (dict, list, or primitive)
        max_depth: Maximum recursion depth to prevent infinite loops

    Returns:
        Sanitized data safe for logging
    """
    if max_depth <= 0:
        return "[MAX_DEPTH_REACHED]"

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            key_lower = str(key).lower()
            if any(sensitive in key_lower for sensitive in SENSITIVE_FIELDS):
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = sanitize_for_logging(value, max_depth - 1)
        return sanitized
    elif isinstance(data, (list, tuple)):
        return [sanitize_for_logging(item, max_depth - 1) for item in data]
    elif isinstance(data, str) and len(data) > Config.MAX_LOG_STRING_LENGTH:
        # Truncate very long strings that might contain sensitive data
        return data[:Config.MAX_LOG_STRING_LENGTH] + "...[TRUNCATED]"
    else:
        return data


class OperationType(str, Enum):
    """Operation types for AI API calls."""
    CHAT = "CHAT"
    EMBED = "EMBED"
    # Future operation types can be added here:
    # IMAGE = "IMAGE"
    # AUDIO = "AUDIO"


# Utility functions for token usage tracking
def get_stop_reason(openai_finish_reason: Optional[str]) -> str:
    """
    Map OpenAI/Azure OpenAI finish reasons to Revenium stop reasons.

    Supports both standard OpenAI and Azure-specific finish reasons.
    All unmapped reasons default to "END" to ensure compatibility.
    """
    finish_reason_map = {
        # Standard OpenAI finish reasons
        "stop": "END",
        "function_call": "END_SEQUENCE",
        "timeout": "TIMEOUT",
        "length": "TOKEN_LIMIT",
        "content_filter": "ERROR",

        # Azure OpenAI specific finish reasons
        "tool_calls": "END_SEQUENCE",  # Modern function calling in Azure
    }

    mapped_reason = finish_reason_map.get(openai_finish_reason or "", "END")

    # Log unmapped finish reasons for monitoring
    if openai_finish_reason and openai_finish_reason not in finish_reason_map:
        logger.warning(f"Unmapped finish reason '{openai_finish_reason}' defaulting to 'END'. "
                      f"Consider adding mapping to ensure accurate stop reason tracking.")

    return mapped_reason


def _validate_extract_usage_inputs(response: Any, operation_type: OperationType,
                                  request_time: str, response_time: str,
                                  request_duration: float) -> None:
    """
    Validate inputs for extract_usage_data function.

    Args:
        response: OpenAI API response object
        operation_type: OperationType enum value
        request_time: ISO formatted request timestamp
        response_time: ISO formatted response timestamp
        request_duration: Request duration in milliseconds

    Raises:
        ValidationError: If any input is invalid
    """
    if response is None:
        raise ValidationError("Response object cannot be None")

    if not isinstance(operation_type, OperationType):
        raise ValidationError(f"operation_type must be OperationType, got {type(operation_type)}")

    if not isinstance(request_time, str) or not request_time.strip():
        raise ValidationError("request_time must be a non-empty string")

    if not isinstance(response_time, str) or not response_time.strip():
        raise ValidationError("response_time must be a non-empty string")

    if not isinstance(request_duration, (int, float)) or request_duration < 0:
        raise ValidationError(f"request_duration must be a non-negative number, got {request_duration}")

    # Validate response has required attributes
    if not hasattr(response, 'model'):
        raise ValidationError("Response object must have 'model' attribute")

    if not hasattr(response, 'usage'):
        raise ValidationError("Response object must have 'usage' attribute")


def extract_usage_data(response, operation_type: OperationType, request_time: str, response_time: str, request_duration: float,
                      client_instance: Optional[Any] = None) -> Tuple[Dict[str, Any], str]:
    """
    Extract usage data from OpenAI/Azure OpenAI API responses.
    Unified function that handles both chat and embeddings responses with provider detection.

    Args:
        response: OpenAI API response object (ChatCompletion or CreateEmbeddingResponse)
        operation_type: OperationType.CHAT or OperationType.EMBED
        request_time: ISO formatted request timestamp
        response_time: ISO formatted response timestamp
        request_duration: Request duration in milliseconds
        client_instance: OpenAI client instance for provider detection

    Returns:
        Tuple of (usage_data dict, transaction_id string)

    Raises:
        ValidationError: If inputs are invalid
    """
    # Validate all inputs before processing
    _validate_extract_usage_inputs(response, operation_type, request_time, response_time, request_duration)
    # Generate transaction ID - embeddings don't have response.id, chats do
    transaction_id = getattr(response, 'id', str(uuid.uuid4()))

    # Detect provider for this request
    provider = detect_provider(client_instance, getattr(client_instance, 'base_url', None) if client_instance else None)
    provider_metadata = get_provider_metadata(provider)

    # Extract raw model name from response
    raw_model_name = response.model

    # Resolve model name for Azure deployments
    if is_azure_provider(provider) and raw_model_name:
        # For Azure, response.model contains deployment name, resolve to LiteLLM model name
        base_url = getattr(client_instance, 'base_url', None) if client_instance else None
        headers = {}  # Headers would need to be passed from wrapper context
        resolved_model_name = resolve_azure_model_name(raw_model_name, base_url, headers)
        logger.debug(f"Azure model resolution: {raw_model_name} -> {resolved_model_name}")
    else:
        resolved_model_name = raw_model_name

    # Extract tokens based on operation type
    if operation_type == OperationType.EMBED:
        input_tokens = response.usage.prompt_tokens
        output_tokens = 0  # Embeddings don't produce output tokens
        total_tokens = response.usage.total_tokens
        stop_reason = "END"  # Embeddings always complete successfully
    else:  # CHAT
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        # Determine finish reason from choices
        openai_finish_reason = response.choices[0].finish_reason if response.choices else None
        stop_reason = get_stop_reason(openai_finish_reason)

    # Extract cached tokens (only available for chat completions)
    cached_tokens = 0
    if operation_type == OperationType.CHAT and hasattr(response.usage, 'prompt_tokens_details'):
        cached_tokens = getattr(response.usage.prompt_tokens_details, 'cached_tokens', 0)

    # Build unified usage data structure
    usage_data = {
        "input_token_count": input_tokens,
        "output_token_count": output_tokens,
        "total_token_count": total_tokens,
        "operation_type": operation_type.value,  # Convert enum to string
        "stop_reason": stop_reason,
        "transaction_id": transaction_id,
        "model": resolved_model_name,  # Use resolved model name for accurate pricing
        "provider": provider_metadata["provider"],
        "model_source": provider_metadata["model_source"],
        "is_streamed": False,  # Will be overridden for streaming
        "time_to_first_token": 0,  # Will be set by caller if applicable
        "cache_creation_token_count": cached_tokens,
        "cache_read_token_count": 0,
        "reasoning_token_count": 0,
        "request_time": request_time,
        "response_time": response_time,
        "completion_start_time": response_time,
        "request_duration": int(request_duration),
        "cost_type": "AI",
        "input_token_cost": None,  # Let backend calculate
        "output_token_cost": None,  # Let backend calculate
        "total_cost": None,  # Let backend calculate
    }

    # Debug logging for provider detection and model resolution
    logger.debug(f"Provider detected: {provider}, metadata: {provider_metadata}")
    logger.debug(f"Model resolution: {raw_model_name} -> {resolved_model_name}")

    logger.debug(
        "Extracted %s usage data - input: %d, output: %d, total: %d, transaction_id: %s",
        operation_type.lower(), input_tokens, output_tokens, total_tokens, transaction_id
    )

    return usage_data, transaction_id


async def log_token_usage(
        response_id: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        cached_tokens: int,
        stop_reason: str,
        request_time: str,
        response_time: str,
        request_duration: int,
        usage_metadata: Dict[str, Any],
        provider: str = "OPENAI",
        model_source: str = "OPENAI",
        system_fingerprint: Optional[str] = None,
        is_streamed: bool = False,
        time_to_first_token: int = 0,
        operation_type: OperationType = OperationType.CHAT  # DEFAULT for backward compatibility
) -> None:
    """Log token usage to Revenium."""
    if shutdown_event.is_set():
        logger.warning("Skipping metering call during shutdown")
        return

    logger.debug("Metering call to Revenium for %s operation %s", operation_type.lower(), response_id)

    # Determine provider - check for OLLAMA first via system fingerprint, then use passed parameters
    if system_fingerprint == "fp_ollama":
        provider = "OLLAMA"
        model_source = "OLLAMA"
        logger.debug(f"OLLAMA provider detected via system_fingerprint: {system_fingerprint}")
    else:
        # Use provider information passed as parameters (already correctly detected for Azure/OpenAI)
        logger.debug(f"Using provider: {provider}, model_source: {model_source}")

    # Create subscriber object from usage metadata
    subscriber = {}

    # Handle nested subscriber object
    if "subscriber" in usage_metadata and isinstance(usage_metadata["subscriber"], dict):
        nested_subscriber = usage_metadata["subscriber"]

        if nested_subscriber.get("id"):
            subscriber["id"] = nested_subscriber["id"]
        if nested_subscriber.get("email"):
            subscriber["email"] = nested_subscriber["email"]
        if nested_subscriber.get("credential") and isinstance(nested_subscriber["credential"], dict):
            # Maintain nested credential structure
            subscriber["credential"] = {
                "name": nested_subscriber["credential"].get("name"),
                "value": nested_subscriber["credential"].get("value")
            }

    # Prepare arguments for create_completion
    completion_args = {
        "cache_creation_token_count": cached_tokens,
        "cache_read_token_count": 0,
        "input_token_cost": None,  # Let backend calculate from model pricing
        "output_token_cost": None,  # Let backend calculate from model pricing
        "total_cost": None,  # Let backend calculate from model pricing
        "output_token_count": completion_tokens,
        "cost_type": "AI",
        "model": model,
        "input_token_count": prompt_tokens,
        "provider": provider,
        "model_source": model_source,
        "reasoning_token_count": 0,
        "request_time": request_time,
        "response_time": response_time,
        "completion_start_time": response_time,
        "request_duration": int(request_duration),
        "stop_reason": stop_reason,
        "total_token_count": total_tokens,
        "transaction_id": response_id,
        "trace_id": usage_metadata.get("trace_id"),
        "task_type": usage_metadata.get("task_type"),
        "subscriber": subscriber if subscriber else None,
        "organization_id": usage_metadata.get("organization_id") or usage_metadata.get("organizationId"),
        "subscription_id": usage_metadata.get("subscription_id"),
        "product_id": usage_metadata.get("product_id"),
        "agent": usage_metadata.get("agent"),
        "response_quality_score": usage_metadata.get("response_quality_score"),
        "is_streamed": is_streamed,
        "operation_type": operation_type.value,  # Convert enum to string
        "time_to_first_token": time_to_first_token,
        "middleware_source": "PYTHON"
    }

    # Log the arguments at debug level
    logger.debug("Calling client.ai.create_completion with args: %s", completion_args)

    # Debug logging for metering call
    logger.debug(f"Metering call for {operation_type.value}: {response_id}, tokens: {prompt_tokens}+{completion_tokens}={total_tokens}")

    try:
        # The client.ai.create_completion method is not async, so don't use await
        result = client.ai.create_completion(**completion_args)
        logger.debug("Metering call result: %s", result)
        logger.debug(f"✅ REVENIUM SUCCESS: Metering call successful: {result.id}")
    except Exception as e:
        if not shutdown_event.is_set():
            # Categorize the exception for better error handling
            categorized_error = categorize_exception(e)
            logger.error(f"❌ REVENIUM FAILURE: {categorized_error}")

            # Use sanitized logging to prevent sensitive data exposure
            sanitized_args = sanitize_for_logging(completion_args)
            logger.error(f"❌ REVENIUM FAILURE: Completion args were: {sanitized_args}")

            # Log the full traceback for better debugging
            import traceback
            logger.error(f"❌ REVENIUM FAILURE: Traceback: {traceback.format_exc()}")
        else:
            logger.debug("Metering call failed during shutdown - this is expected")


def create_metering_call(response, operation_type: OperationType, request_time_dt, usage_metadata,
                        client_instance: Optional[Any] = None, time_to_first_token: int = 0, is_streamed: bool = False):
    """
    Unified function to create and execute metering calls for any operation type.
    Reduces duplication between chat and embeddings wrappers.
    """
    # Record timing
    response_time_dt = datetime.datetime.now(datetime.timezone.utc)
    response_time = response_time_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    request_time = request_time_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    request_duration = (response_time_dt - request_time_dt).total_seconds() * 1000

    # Extract usage data using unified function
    usage_data, transaction_id = extract_usage_data(
        response, operation_type, request_time, response_time, request_duration, client_instance
    )

    # Override streaming and timing info
    usage_data["is_streamed"] = is_streamed
    usage_data["time_to_first_token"] = time_to_first_token

    # Get system fingerprint if available (chat only)
    system_fingerprint = getattr(response, 'system_fingerprint', None)

    # Create async metering call
    async def metering_call():
        await log_token_usage(
            response_id=transaction_id,
            model=usage_data["model"],
            prompt_tokens=usage_data["input_token_count"],
            completion_tokens=usage_data["output_token_count"],
            total_tokens=usage_data["total_token_count"],
            cached_tokens=usage_data["cache_creation_token_count"],
            stop_reason=usage_data["stop_reason"],
            request_time=usage_data["request_time"],
            response_time=usage_data["response_time"],
            request_duration=usage_data["request_duration"],
            usage_metadata=usage_metadata,
            provider=usage_data["provider"],
            model_source=usage_data["model_source"],
            system_fingerprint=system_fingerprint,
            is_streamed=is_streamed,
            time_to_first_token=time_to_first_token,
            operation_type=operation_type  # Explicitly pass the operation type
        )

    # Start metering thread
    thread = run_async_in_thread(metering_call())
    logger.debug("%s metering thread started: %s", operation_type, thread)
    return thread


def _extract_langchain_usage_metadata():
    """
    Extract usage_metadata from LangChain context variables.

    LangChain stores context information in thread-local variables that we can access
    to get the usage_metadata that was passed to LangChain methods.
    """
    try:
        # Try to import LangChain context variables
        from langchain_core.globals import get_llm_cache
        from langchain_core.callbacks.manager import CallbackManagerForLLMRun
        import contextvars

        # Try to get the current context
        # LangChain uses context variables to store run information
        # We need to look for the current callback manager or run context

        # Check if we're in a LangChain context by looking for context variables
        # This is a best-effort approach since LangChain's internal context handling
        # can vary between versions

        # Look for common LangChain context patterns
        import inspect
        frame = inspect.currentframe()

        # Walk up the call stack to find LangChain frames
        while frame:
            frame_locals = frame.f_locals
            frame_globals = frame.f_globals

            # Look for LangChain-specific variables in the call stack
            # Check for 'config' parameter which often contains metadata
            if 'config' in frame_locals and isinstance(frame_locals['config'], dict):
                config = frame_locals['config']
                if 'metadata' in config and isinstance(config['metadata'], dict):
                    metadata = config['metadata']
                    if 'usage_metadata' in metadata:
                        logger.debug(f"Found usage_metadata in LangChain config: {metadata['usage_metadata']}")
                        return metadata['usage_metadata']

            # Check for 'metadata' parameter directly
            if 'metadata' in frame_locals and isinstance(frame_locals['metadata'], dict):
                metadata = frame_locals['metadata']
                if 'usage_metadata' in metadata:
                    logger.debug(f"Found usage_metadata in LangChain metadata: {metadata['usage_metadata']}")
                    return metadata['usage_metadata']

            # Check for callback manager with metadata
            if 'callback_manager' in frame_locals:
                cb_manager = frame_locals['callback_manager']
                if hasattr(cb_manager, 'metadata') and isinstance(cb_manager.metadata, dict):
                    if 'usage_metadata' in cb_manager.metadata:
                        logger.debug(f"Found usage_metadata in callback manager: {cb_manager.metadata['usage_metadata']}")
                        return cb_manager.metadata['usage_metadata']

            frame = frame.f_back

        logger.debug("No usage_metadata found in LangChain context")
        return {}

    except Exception as e:
        logger.debug(f"Error extracting LangChain usage_metadata: {e}")
        return {}


@wrapt.patch_function_wrapper('openai.resources.embeddings', 'Embeddings.create')
def embeddings_create_wrapper(wrapped, instance, args, kwargs):
    """Wraps the openai.embeddings.create method to log token usage."""
    logger.debug("OpenAI/Azure OpenAI embeddings.create wrapper called")

    # Extract usage metadata and store it for later use
    usage_metadata = kwargs.pop("usage_metadata", {})

    # Try to extract usage_metadata from LangChain context if not found in kwargs
    if not usage_metadata:
        usage_metadata = _extract_langchain_usage_metadata()

    # Record request time
    request_time_dt = datetime.datetime.now(datetime.timezone.utc)
    logger.debug(f"Calling wrapped embeddings function with args: {args}, kwargs: {kwargs}")

    # Call the original OpenAI function
    response = wrapped(*args, **kwargs)

    logger.debug("Handling embeddings response: %s", response)

    # Create metering call using unified function - pass client instance for provider detection
    create_metering_call(response, OperationType.EMBED, request_time_dt, usage_metadata,
                        client_instance=getattr(instance, '_client', None))

    return response


@wrapt.patch_function_wrapper('openai.resources.chat.completions', 'Completions.create')
def create_wrapper(wrapped, instance, args, kwargs):
    """
    Wraps the openai.ChatCompletion.create method to log token usage.
    Handles both streaming and non-streaming responses for OpenAI and Azure OpenAI.
    """
    logger.debug("OpenAI/Azure OpenAI chat.completions.create wrapper called")

    # Extract usage metadata and store it for later use
    usage_metadata = kwargs.pop("usage_metadata", {})

    # Try to extract usage_metadata from LangChain context if not found in kwargs
    if not usage_metadata:
        usage_metadata = _extract_langchain_usage_metadata()

    # Check if this is a streaming request
    stream = kwargs.get('stream', False)

    # If streaming, add stream_options to include usage information
    if stream:
        # Initialize stream_options if it doesn't exist
        if 'stream_options' not in kwargs:
            kwargs['stream_options'] = {}
        # Add include_usage flag to get token counts in the response
        kwargs['stream_options']['include_usage'] = True
        logger.debug("Added include_usage to stream_options for accurate token counting in streaming response")

    # Record request time
    request_time_dt = datetime.datetime.now(datetime.timezone.utc)
    logger.debug(f"Calling wrapped function with args: {args}, kwargs: {kwargs}")

    # Call the original OpenAI function
    response = wrapped(*args, **kwargs)

    # Record time to first token (for non-streaming, this is the same as the full response time)
    first_token_time_dt = datetime.datetime.now(datetime.timezone.utc)
    time_to_first_token = int((first_token_time_dt - request_time_dt).total_seconds() * 1000)

    # Handle based on response type
    if stream:
        # For streaming responses (openai.Stream)
        logger.debug("Handling streaming response")
        return handle_streaming_response(
            response,
            request_time_dt,
            usage_metadata,
            client_instance=getattr(instance, '_client', None)
        )
    else:
        # For non-streaming responses (ChatCompletion)
        logger.debug("Handling non-streaming response: %s", response)

        # Create metering call using unified function - pass client instance for provider detection
        create_metering_call(response, OperationType.CHAT, request_time_dt, usage_metadata,
                            client_instance=getattr(instance, '_client', None), time_to_first_token=time_to_first_token)

        return response


def handle_streaming_response(stream, request_time_dt, usage_metadata, client_instance: Optional[Any] = None):
    """
    Handle streaming responses from OpenAI/Azure OpenAI.
    Wraps the stream to collect metrics and log them after completion.
    Similar to the approach used in the Ollama middleware.
    """

    # Create a wrapper for the streaming response with proper resource management
    class StreamWrapper:
        def __init__(self, stream):
            self.stream = stream
            self.chunks = []
            self.response_id = None
            self.model = None
            self.finish_reason = None
            self.system_fingerprint = None
            self.request_time_dt = request_time_dt
            self.usage_metadata = usage_metadata
            self.final_usage = None
            self.completion_text = ""
            self.first_token_time = None
            self.client_instance = client_instance  # Store for Azure provider detection
            self._closed = False
            self._usage_logged = False

        def __iter__(self):
            return self

        def __next__(self):
            if self._closed:
                raise StopIteration("Stream has been closed")

            try:
                chunk = next(self.stream)
                self._process_chunk(chunk)
                return chunk
            except StopIteration:
                self._finalize()
                raise
            except Exception as e:
                # Ensure cleanup on any error
                self._finalize()
                logger.error(f"Error in streaming response: {e}")
                raise

        def __enter__(self):
            """Context manager entry."""
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            """Context manager exit with cleanup."""
            self._finalize()

        def _finalize(self):
            """Finalize the stream and log usage if not already done."""
            if not self._usage_logged:
                self._log_usage()
                self._usage_logged = True
            self._close_stream()

        def _close_stream(self):
            """Close the underlying stream if possible."""
            if not self._closed:
                try:
                    if hasattr(self.stream, 'close'):
                        self.stream.close()
                except Exception as e:
                    logger.debug(f"Error closing stream: {e}")
                finally:
                    self._closed = True

        def _process_chunk(self, chunk):
            # Extract response ID and model from the chunk if available
            if self.response_id is None and hasattr(chunk, 'id'):
                self.response_id = chunk.id
            if self.model is None and hasattr(chunk, 'model'):
                self.model = chunk.model
            if self.system_fingerprint is None and hasattr(chunk, 'system_fingerprint'):
                self.system_fingerprint = chunk.system_fingerprint
                logger.debug(f"Captured system_fingerprint from stream chunk: {self.system_fingerprint}")
            else:
                logger.debug(f"System fingerprint already set: {self.system_fingerprint}")


            # Check for finish reason in the chunk
            if chunk.choices and chunk.choices[0].finish_reason:
                self.finish_reason = chunk.choices[0].finish_reason

            # Check if this is the special usage chunk (last chunk with empty choices array)
            if hasattr(chunk, 'usage') and chunk.usage and (not chunk.choices or len(chunk.choices) == 0):
                logger.debug(f"Found usage data in final chunk: {chunk.usage}")
                self.final_usage = chunk.usage
                return

            # Collect content for token estimation if needed
            if chunk.choices and hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content') and \
                    chunk.choices[0].delta.content:
                # Record time of first token if not already set
                if self.first_token_time is None:
                    self.first_token_time = datetime.datetime.now(datetime.timezone.utc)
                self.completion_text += chunk.choices[0].delta.content

            # Store the chunk for later analysis
            self.chunks.append(chunk)

        def _log_usage(self):
            if not self.chunks:
                return

            # Record response time and calculate duration
            response_time_dt = datetime.datetime.now(datetime.timezone.utc)
            response_time = response_time_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            request_duration = (response_time_dt - self.request_time_dt).total_seconds() * 1000

            # Get token usage information
            prompt_tokens = 0
            completion_tokens = 0
            total_tokens = 0
            cached_tokens = 0

            # First check if we have the final usage data from the special chunk
            if self.final_usage:
                prompt_tokens = self.final_usage.prompt_tokens
                completion_tokens = self.final_usage.completion_tokens
                total_tokens = self.final_usage.total_tokens
                # Check if we have cached tokens info
                if hasattr(self.final_usage, 'prompt_tokens_details') and hasattr(
                        self.final_usage.prompt_tokens_details, 'cached_tokens'):
                    cached_tokens = self.final_usage.prompt_tokens_details.cached_tokens
                logger.debug(
                    f"Using token usage from final chunk: prompt={prompt_tokens}, completion={completion_tokens}, total={total_tokens}")
            else:
                # If we don't have usage data, estimate from content
                logger.warning("No usage data found in streaming response!")

            stop_reason = get_stop_reason(self.finish_reason)

            # Log the token usage
            if self.response_id:
                logger.debug(
                    "Streaming token usage - response_id: %s, prompt: %d, completion: %d, total: %d",
                    self.response_id, prompt_tokens, completion_tokens, total_tokens
                )

                # Detect provider and resolve model name for Azure
                provider = detect_provider(self.client_instance,
                                         getattr(self.client_instance, 'base_url', None) if self.client_instance else None)
                provider_metadata = get_provider_metadata(provider)

                # Resolve model name for Azure deployments
                raw_model_name = self.model or "unknown"
                if is_azure_provider(provider) and raw_model_name != "unknown":
                    base_url = getattr(self.client_instance, 'base_url', None) if self.client_instance else None
                    headers = {}  # Headers would need to be passed from wrapper context
                    resolved_model_name = resolve_azure_model_name(raw_model_name, base_url, headers)
                    logger.debug(f"Azure streaming model resolution: {raw_model_name} -> {resolved_model_name}")
                else:
                    resolved_model_name = raw_model_name

                # Calculate time to first token if available
                time_to_first_token = 0
                if self.first_token_time:
                    time_to_first_token = int((self.first_token_time - self.request_time_dt).total_seconds() * 1000)
                    logger.debug(f"Time to first token: {time_to_first_token}ms")

                async def metering_call():
                    await log_token_usage(
                        response_id=self.response_id,
                        model=resolved_model_name,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        total_tokens=total_tokens,
                        cached_tokens=cached_tokens,
                        stop_reason=stop_reason,
                        request_time=self.request_time_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        response_time=response_time,
                        request_duration=int(request_duration),
                        usage_metadata=self.usage_metadata,
                        provider=provider_metadata["provider"],
                        model_source=provider_metadata["model_source"],
                        system_fingerprint=self.system_fingerprint,
                        is_streamed=True,
                        time_to_first_token=time_to_first_token,
                        operation_type=OperationType.CHAT,
                    )

                thread = run_async_in_thread(metering_call())
                logger.debug("Streaming metering thread started: %s", thread)

    # Return the wrapped stream
    return StreamWrapper(iter(stream))
