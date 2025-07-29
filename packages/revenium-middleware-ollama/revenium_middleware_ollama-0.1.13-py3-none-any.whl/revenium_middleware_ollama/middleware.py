import logging
import datetime
import wrapt
import types

logger = logging.getLogger("revenium_middleware.extension")

from revenium_middleware import client, run_async_in_thread, shutdown_event


@wrapt.patch_function_wrapper('ollama', 'chat')
def chat_wrapper(wrapped, _, args, kwargs):
    """
    Wraps the ollama.chat method to log token usage.
    Handles both streaming and non-streaming responses.
    """
    logger.debug("Ollama chat wrapper called")
    usage_metadata = kwargs.pop("usage_metadata", {}) if "usage_metadata" in kwargs else {}
    is_streaming = kwargs.get("stream", False)

    # If streaming is enabled, add stream_options to include usage information
    # if is_streaming and "stream_options" not in kwargs:
    #     kwargs["stream_options"] = {"include_usage": True}
    # elif is_streaming and isinstance(kwargs.get("stream_options"), dict):
    #     kwargs["stream_options"]["include_usage"] = True

    request_time_dt = datetime.datetime.now(datetime.timezone.utc)
    logger.debug(f"Calling chat function with args: {args}, kwargs: {kwargs}")

    response = wrapped(*args, **kwargs)

    # Check if response is a generator (streaming response)
    if is_streaming and isinstance(response, types.GeneratorType):
        return handle_streaming_response(response, request_time_dt, usage_metadata)
    else:
        # Handle non-streaming response
        logger.debug("Ollama chat response: %s", response)
        handle_response(response, request_time_dt, usage_metadata, False)
        return response


@wrapt.patch_function_wrapper('ollama', 'generate')
def generate_wrapper(wrapped, _, args, kwargs):
    """
    Wraps the ollama.generate method to log token usage.
    Handles both streaming and non-streaming responses.
    """
    logger.debug("Ollama generate wrapper called")
    usage_metadata = kwargs.pop("usage_metadata", {}) if "usage_metadata" in kwargs else {}
    is_streaming = kwargs.get("stream", False)

    # If streaming is enabled, add stream_options to include usage information
    if is_streaming and "stream_options" not in kwargs:
        kwargs["stream_options"] = {"include_usage": True}
    elif is_streaming and isinstance(kwargs.get("stream_options"), dict):
        kwargs["stream_options"]["include_usage"] = True

    request_time_dt = datetime.datetime.now(datetime.timezone.utc)
    logger.debug(f"Calling generate function with args: {args}, kwargs: {kwargs}")

    response = wrapped(*args, **kwargs)

    # Check if response is a generator (streaming response)
    if is_streaming and isinstance(response, types.GeneratorType):
        return handle_streaming_response(response, request_time_dt, usage_metadata)
    else:
        # Handle non-streaming response
        logger.debug("Ollama generate response: %s", response)
        handle_response(response, request_time_dt, usage_metadata, False)
        return response


def handle_streaming_response(generator, request_time_dt, usage_metadata):
    """
    Handles streaming responses by collecting all chunks and processing the final state.
    Returns a new generator that yields the same chunks.
    """
    chunks = []
    final_response = None

    def wrapped_generator():
        nonlocal chunks, final_response

        # Collect all chunks
        for chunk in generator:
            chunks.append(chunk)
            yield chunk

        # After all chunks are processed, construct the final response
        if chunks:
            # The last chunk should contain the complete response data
            final_response = chunks[-1]
            handle_response(final_response, request_time_dt, usage_metadata, True)

    return wrapped_generator()


def handle_response(response, request_time_dt, usage_metadata, is_streaming):
    """
    Process a complete response (either streaming or non-streaming) and send metering data.
    """

    async def metering_call():
        response_time_dt = datetime.datetime.now(datetime.timezone.utc)
        response_time = response_time_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        request_duration = (response_time_dt - request_time_dt).total_seconds() * 1000
        request_time = request_time_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Generate a unique ID if not present in response
        response_id = getattr(response, 'id', f"ollama-{datetime.datetime.now().timestamp()}")

        # Extract token counts from Ollama response
        prompt_tokens = getattr(response, 'prompt_eval_count', 0)
        completion_tokens = getattr(response, 'eval_count', 0)
        total_tokens = prompt_tokens + completion_tokens
        cached_tokens = 0  # Ollama doesn't provide cached tokens info

        logger.debug(
            "Ollama chat token usage - prompt: %d, completion: %d, total: %d",
            prompt_tokens, completion_tokens, total_tokens
        )

        ollama_finish_reason = getattr(response, 'done_reason', None)

        finish_reason_map = {
            "stop": "END",
            "length": "TOKEN_LIMIT",
            "error": "ERROR",
            "cancelled": "CANCELLED",
            "tool_calls": "END_SEQUENCE"
        }
        stop_reason = finish_reason_map.get(ollama_finish_reason, "END")  # type: ignore

        try:
            if shutdown_event.is_set():
                logger.warning("Skipping metering call during shutdown")
                return
            logger.debug("Metering call to Revenium for completion %s", response_id)

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
                "input_token_cost": None,
                "output_token_cost": None,
                "total_cost": None,
                "output_token_count": completion_tokens,
                "cost_type": "AI",
                "model": getattr(response, 'model', 'ollama-model'),
                "input_token_count": prompt_tokens,
                "provider": "OLLAMA",
                "model_source": "OLLAMA",
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
                "organization_id": usage_metadata.get("organization_id"),
                "subscription_id": usage_metadata.get("subscription_id"),
                "product_id": usage_metadata.get("product_id"),
                "agent": usage_metadata.get("agent"),
                "is_streamed": is_streaming,
            }

            # Log the arguments at debug level
            logger.debug("Arguments for create_completion: %s", completion_args)

            # The client.ai.create_completion method is not async, so don't use await
            result = client.ai.create_completion(**completion_args)
            logger.debug("Metering call result: %s", result)
        except Exception as e:
            if not shutdown_event.is_set():
                logger.warning(f"Error in metering call: {str(e)}")
                # Log the full traceback for better debugging
                import traceback
                logger.warning(f"Traceback: {traceback.format_exc()}")

    thread = run_async_in_thread(metering_call())
    logger.debug("Metering thread started: %s", thread)
