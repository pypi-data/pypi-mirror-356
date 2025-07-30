"""
Client wrapper functions for comprehensive LLM monitoring and tracing.

This module provides wrapper functions that intercept LLM client calls to add:
- MLflow tracing with spans
- Cost tracking
- Token usage monitoring
- Support for both streaming and non-streaming responses
"""

import asyncio
import functools
import time
import uuid
import mlflow

from autonomize_observer.utils import setup_logger

logger = setup_logger(__name__)


def wrap_openai_async_with_separate_runs(client, cost_tracker, mlflow_client):
    """Wrap OpenAI async client with separate runs for each LLM call."""
    if hasattr(client, "chat") and hasattr(client.chat, "completions"):
        if (
            hasattr(client.chat.completions, "create")
            and callable(client.chat.completions.create)
            and client.__class__.__name__ == "AsyncOpenAI"
        ):
            original_async_create = client.chat.completions.create

            async def wrapped_async_create(*args, **kwargs):
                # Check if MLflow autolog is handling the run
                active_run = mlflow.active_run()
                should_manage_run = active_run is None

                if should_manage_run:
                    # Only create our own run if MLflow autolog isn't managing one
                    run_name = f"async_llm_call_{uuid.uuid4().hex[:8]}"
                    run = mlflow.start_run(run_name=run_name)
                else:
                    run = active_run

                # Create trace/span for this LLM call
                model_name = kwargs.get("model", "gpt-3.5-turbo")
                span_name = f"openai_chat_completion_{model_name}"

                try:
                    # Try to use MLflow 3.x tracing API
                    with mlflow.start_span(name=span_name) as span:
                        # Set span inputs using set_inputs (MLflow 3.x API)
                        inputs = {
                            "model": model_name,
                            "provider": "openai",
                            "async": True,
                            "messages": kwargs.get("messages", []),
                        }
                        if "temperature" in kwargs:
                            inputs["temperature"] = kwargs["temperature"]
                        if "max_tokens" in kwargs:
                            inputs["max_tokens"] = kwargs["max_tokens"]

                        span.set_inputs(inputs)

                        result = await original_async_create(*args, **kwargs)

                        # Handle streaming vs non-streaming responses
                        is_streaming = kwargs.get("stream", False)

                        if is_streaming:
                            # For streaming, we can't get the full response content immediately
                            outputs = {
                                "response": "[Streaming response - content not available during span creation]",
                                "streaming": True,
                            }
                            span.set_outputs(outputs)
                            # Note: Cost tracking for streaming responses would need to be handled
                            # after the stream is consumed, which is outside this wrapper's scope
                        else:
                            # Non-streaming response
                            outputs = {
                                "response": (
                                    result.choices[0].message.content
                                    if result.choices
                                    else ""
                                ),
                                "streaming": False,
                            }

                            if hasattr(result, "usage") and result.usage:
                                prompt_tokens = result.usage.prompt_tokens
                                completion_tokens = result.usage.completion_tokens
                                outputs.update(
                                    {
                                        "prompt_tokens": prompt_tokens,
                                        "completion_tokens": completion_tokens,
                                        "total_tokens": result.usage.total_tokens,
                                    }
                                )

                                # Track cost regardless of who manages the run
                                cost_tracker.track_cost(
                                    model_name=model_name,
                                    input_tokens=prompt_tokens,
                                    output_tokens=completion_tokens,
                                    run_id=run.info.run_id,
                                )

                            span.set_outputs(outputs)

                        return result

                except (AttributeError, ImportError):
                    # Fallback for older MLflow versions or if tracing not available
                    logger.debug("MLflow tracing not available, using basic monitoring")
                    result = await original_async_create(*args, **kwargs)

                    # Track cost regardless of who manages the run
                    if hasattr(result, "usage") and result.usage:
                        prompt_tokens = result.usage.prompt_tokens
                        completion_tokens = result.usage.completion_tokens
                        cost_tracker.track_cost(
                            model_name=model_name,
                            input_tokens=prompt_tokens,
                            output_tokens=completion_tokens,
                            run_id=run.info.run_id,
                        )

                    return result

                finally:
                    # Log model parameter and end run only if we're managing the run
                    if should_manage_run:
                        try:
                            if mlflow_client:
                                mlflow_client.log_param("model", model_name)
                            else:
                                mlflow.log_param("model", model_name)
                        except Exception as e:
                            logger.warning(f"Could not log model parameter: {e}")

                        mlflow.end_run()

            client.chat.completions.create = wrapped_async_create


def wrap_openai_sync_with_separate_runs(client, cost_tracker, mlflow_client):
    """Wrap OpenAI sync client with separate runs for each LLM call."""
    if hasattr(client.chat, "completions") and hasattr(
        client.chat.completions, "create"
    ):
        original_create = client.chat.completions.create

        def wrapped_create(*args, **kwargs):
            # Check if MLflow autolog is handling the run
            active_run = mlflow.active_run()
            should_manage_run = active_run is None

            if should_manage_run:
                # Only create our own run if MLflow autolog isn't managing one
                run_name = f"llm_call_{uuid.uuid4().hex[:8]}"
                run = mlflow.start_run(run_name=run_name)
            else:
                run = active_run

            # Create trace/span for this LLM call
            model_name = kwargs.get("model", "gpt-3.5-turbo")
            span_name = f"openai_chat_completion_{model_name}"

            try:
                # Try to use MLflow 3.x tracing API
                with mlflow.start_span(name=span_name) as span:
                    # Set span inputs using set_inputs (MLflow 3.x API)
                    inputs = {
                        "model": model_name,
                        "provider": "openai",
                        "async": False,
                        "messages": kwargs.get("messages", []),
                    }
                    if "temperature" in kwargs:
                        inputs["temperature"] = kwargs["temperature"]
                    if "max_tokens" in kwargs:
                        inputs["max_tokens"] = kwargs["max_tokens"]

                    span.set_inputs(inputs)

                    result = original_create(*args, **kwargs)

                    # Handle streaming vs non-streaming responses
                    is_streaming = kwargs.get("stream", False)

                    if is_streaming:
                        # For streaming, we can't get the full response content immediately
                        outputs = {
                            "response": "[Streaming response - content not available during span creation]",
                            "streaming": True,
                        }
                        span.set_outputs(outputs)
                        # Note: Cost tracking for streaming responses would need to be handled
                        # after the stream is consumed, which is outside this wrapper's scope
                    else:
                        # Non-streaming response
                        outputs = {
                            "response": (
                                result.choices[0].message.content
                                if result.choices
                                else ""
                            ),
                            "streaming": False,
                        }

                        if hasattr(result, "usage") and result.usage:
                            prompt_tokens = result.usage.prompt_tokens
                            completion_tokens = result.usage.completion_tokens
                            outputs.update(
                                {
                                    "prompt_tokens": prompt_tokens,
                                    "completion_tokens": completion_tokens,
                                    "total_tokens": result.usage.total_tokens,
                                }
                            )

                            # Track cost regardless of who manages the run
                            cost_tracker.track_cost(
                                model_name=model_name,
                                input_tokens=prompt_tokens,
                                output_tokens=completion_tokens,
                                run_id=run.info.run_id,
                            )

                        span.set_outputs(outputs)

                    return result

            except (AttributeError, ImportError):
                # Fallback for older MLflow versions or if tracing not available
                logger.debug("MLflow tracing not available, using basic monitoring")
                result = original_create(*args, **kwargs)

                # Track cost regardless of who manages the run
                if hasattr(result, "usage") and result.usage:
                    prompt_tokens = result.usage.prompt_tokens
                    completion_tokens = result.usage.completion_tokens
                    cost_tracker.track_cost(
                        model_name=model_name,
                        input_tokens=prompt_tokens,
                        output_tokens=completion_tokens,
                        run_id=run.info.run_id,
                    )

                return result

            finally:
                # Log model parameter and end run only if we're managing the run
                if should_manage_run:
                    try:
                        if mlflow_client:
                            mlflow_client.log_param("model", model_name)
                        else:
                            mlflow.log_param("model", model_name)
                    except Exception as e:
                        logger.warning(f"Could not log model parameter: {e}")

                    mlflow.end_run()

        client.chat.completions.create = wrapped_create


def wrap_anthropic_async_with_separate_runs(client, cost_tracker, mlflow_client):
    """Wrap Anthropic async client with separate runs for each LLM call."""
    if hasattr(client, "messages") and hasattr(client.messages, "acreate"):
        original_acreate = client.messages.acreate

        async def wrapped_acreate(*args, **kwargs):
            # Check if MLflow autolog is handling the run
            active_run = mlflow.active_run()
            should_manage_run = active_run is None

            if should_manage_run:
                # Only create our own run if MLflow autolog isn't managing one
                run_name = f"async_anthropic_call_{uuid.uuid4().hex[:8]}"
                run = mlflow.start_run(run_name=run_name)
            else:
                run = active_run

            # Create trace/span for this LLM call
            model_name = kwargs.get("model", "anthropic-default")
            span_name = f"anthropic_messages_{model_name}"

            try:
                # Try to use MLflow 3.x tracing API
                with mlflow.start_span(name=span_name) as span:
                    # Set span inputs using set_inputs (MLflow 3.x API)
                    inputs = {
                        "model": model_name,
                        "provider": "anthropic",
                        "async": True,
                        "messages": kwargs.get("messages", []),
                    }
                    if "temperature" in kwargs:
                        inputs["temperature"] = kwargs["temperature"]
                    if "max_tokens" in kwargs:
                        inputs["max_tokens"] = kwargs["max_tokens"]

                    span.set_inputs(inputs)

                    result = await original_acreate(*args, **kwargs)

                    # Set span outputs
                    outputs = {
                        "response": result.content[0].text if result.content else "",
                    }

                    if hasattr(result, "usage") and result.usage:
                        prompt_tokens = result.usage.input_tokens
                        completion_tokens = result.usage.output_tokens
                        outputs.update(
                            {
                                "input_tokens": prompt_tokens,
                                "output_tokens": completion_tokens,
                                "total_tokens": prompt_tokens + completion_tokens,
                            }
                        )

                        # Track cost regardless of who manages the run
                        cost_tracker.track_cost(
                            model_name=model_name,
                            input_tokens=prompt_tokens,
                            output_tokens=completion_tokens,
                            run_id=run.info.run_id,
                        )

                    span.set_outputs(outputs)
                    return result

            except (AttributeError, ImportError):
                # Fallback for older MLflow versions or if tracing not available
                logger.debug("MLflow tracing not available, using basic monitoring")
                result = await original_acreate(*args, **kwargs)

                # Track cost regardless of who manages the run
                if hasattr(result, "usage") and result.usage:
                    prompt_tokens = result.usage.input_tokens
                    completion_tokens = result.usage.output_tokens
                    cost_tracker.track_cost(
                        model_name=model_name,
                        input_tokens=prompt_tokens,
                        output_tokens=completion_tokens,
                        run_id=run.info.run_id,
                    )

                return result

            finally:
                # Log model parameter and end run only if we're managing the run
                if should_manage_run:
                    try:
                        if mlflow_client:
                            mlflow_client.log_param("model", model_name)
                        else:
                            mlflow.log_param("model", model_name)
                    except Exception as e:
                        logger.warning(f"Could not log model parameter: {e}")

                    mlflow.end_run()

        client.messages.acreate = wrapped_acreate


def wrap_anthropic_sync_with_separate_runs(client, cost_tracker, mlflow_client):
    """Wrap Anthropic sync client with separate runs for each LLM call."""
    if hasattr(client, "messages") and hasattr(client.messages, "create"):
        original_create = client.messages.create

        def wrapped_create(*args, **kwargs):
            # Check if MLflow autolog is handling the run
            active_run = mlflow.active_run()
            should_manage_run = active_run is None

            if should_manage_run:
                # Only create our own run if MLflow autolog isn't managing one
                run_name = f"anthropic_call_{uuid.uuid4().hex[:8]}"
                run = mlflow.start_run(run_name=run_name)
            else:
                run = active_run

            # Create trace/span for this LLM call
            model_name = kwargs.get("model", "anthropic-default")
            span_name = f"anthropic_messages_{model_name}"

            try:
                # Try to use MLflow 3.x tracing API
                with mlflow.start_span(name=span_name) as span:
                    # Set span inputs using set_inputs (MLflow 3.x API)
                    inputs = {
                        "model": model_name,
                        "provider": "anthropic",
                        "async": False,
                        "messages": kwargs.get("messages", []),
                    }
                    if "temperature" in kwargs:
                        inputs["temperature"] = kwargs["temperature"]
                    if "max_tokens" in kwargs:
                        inputs["max_tokens"] = kwargs["max_tokens"]

                    span.set_inputs(inputs)

                    result = original_create(*args, **kwargs)

                    # Set span outputs
                    outputs = {
                        "response": result.content[0].text if result.content else "",
                    }

                    if hasattr(result, "usage") and result.usage:
                        prompt_tokens = result.usage.input_tokens
                        completion_tokens = result.usage.output_tokens
                        outputs.update(
                            {
                                "input_tokens": prompt_tokens,
                                "output_tokens": completion_tokens,
                                "total_tokens": prompt_tokens + completion_tokens,
                            }
                        )

                        # Track cost regardless of who manages the run
                        cost_tracker.track_cost(
                            model_name=model_name,
                            input_tokens=prompt_tokens,
                            output_tokens=completion_tokens,
                            run_id=run.info.run_id,
                        )

                    span.set_outputs(outputs)
                    return result

            except (AttributeError, ImportError):
                # Fallback for older MLflow versions or if tracing not available
                logger.debug("MLflow tracing not available, using basic monitoring")
                result = original_create(*args, **kwargs)

                # Track cost regardless of who manages the run
                if hasattr(result, "usage") and result.usage:
                    prompt_tokens = result.usage.input_tokens
                    completion_tokens = result.usage.output_tokens
                    cost_tracker.track_cost(
                        model_name=model_name,
                        input_tokens=prompt_tokens,
                        output_tokens=completion_tokens,
                        run_id=run.info.run_id,
                    )

                return result

            finally:
                # Log model parameter and end run only if we're managing the run
                if should_manage_run:
                    try:
                        if mlflow_client:
                            mlflow_client.log_param("model", model_name)
                        else:
                            mlflow.log_param("model", model_name)
                    except Exception as e:
                        logger.warning(f"Could not log model parameter: {e}")

                    mlflow.end_run()

        client.messages.create = wrapped_create
