"""
Instrumentor for HuggingFace Transformers Pipelines.

This module provides an instrumentor that wraps HuggingFace pipeline calls
to automatically capture inputs, outputs, token usage, and costs,
logging them to the active LLMTrace session.
"""
import functools
from typing import Any, Callable, TypeVar, ParamSpec, List, Dict, Optional
from llmtrace.core.core import log_message, log_metric, log_error, get_current_session_id
from llmtrace.tracing.models import Message
from llmtrace.instrumentation.base import BaseInstrumentor
import asyncio

P = ParamSpec("P")
R = TypeVar("R")

# --- Mock HuggingFace Transformers for demonstration purposes ---
class MockTokenizer:
    """A mock tokenizer for simulating token encoding/decoding."""
    def encode(self, text: str) -> List[int]:
        """
        Simulates encoding text into token IDs.

        :param text: The input text string.
        :type text: str
        :returns: A list of simulated token IDs.
        :rtype: List[int]
        """
        return list(range(len(text.split())))
    def decode(self, tokens: List[int]) -> str:
        """
        Simulates decoding token IDs back to text.

        :param tokens: A list of token IDs.
        :type tokens: List[int]
        :returns: A simulated decoded text string.
        :rtype: str
        """
        return " ".join([str(t) for t in tokens])

class MockPipeline:
    """
    A mock HuggingFace pipeline for simulating LLM calls.

    This class mimics the behavior of a HuggingFace Transformers pipeline
    for testing and demonstration purposes, including token usage and cost estimation.
    """
    def __init__(self, task: str = "text-generation", model: str = "mock-model"):
        """
        Initializes the mock pipeline.

        :param task: The task the pipeline performs (e.g., "text-generation").
        :type task: str
        :param model: The name of the model used by the pipeline.
        :type model: str
        """
        self.task = task
        self.model = model
        self.tokenizer = MockTokenizer()
        print(f"Mock HuggingFace Pipeline initialized: {task} with {model}")

    async def __call__(self, inputs: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Simulates an asynchronous call to the HuggingFace pipeline.

        :param inputs: The input to the pipeline (e.g., text string or list of strings).
        :type inputs: Any
        :param kwargs: Additional keyword arguments passed to the pipeline.
        :type kwargs: Any
        :returns: A list of dictionaries containing generated text and token info.
        :rtype: List[Dict[str, Any]]
        """
        print(f"Mock HuggingFace: Calling pipeline for task '{self.task}' with inputs: {inputs}")
        await asyncio.sleep(0.05)
        
        input_text = " ".join(inputs) if isinstance(inputs, list) else inputs

        generated_text = f"Mock generated text for: '{input_text[:50]}...'"
        
        prompt_tokens = len(self.tokenizer.encode(input_text))
        completion_tokens = len(self.tokenizer.encode(generated_text))
        total_tokens = prompt_tokens + completion_tokens
        
        cost = (total_tokens / 1000) * 0.001

        return [{"generated_text": generated_text, "tokens": {"prompt": prompt_tokens, "completion": completion_tokens, "total": total_tokens, "cost": cost}}]

# ----------------------------------------------------------------

class HFInstrumentor(BaseInstrumentor):
    """
    Instrumentor for HuggingFace Transformers Pipelines.

    Wraps the `__call__` method of a given pipeline object to log its inputs,
    outputs, token usage, and estimated cost to the active LLMTrace session.
    """
    def __init__(self):
        """
        Initializes the HFInstrumentor.
        Stores a mapping of instrumented pipeline object IDs to their original `__call__` methods.
        """
        self._instrumented_pipelines: Dict[int, Callable[..., Any]] = {}

    def instrument(self, pipeline_obj: Any) -> None:
        """
        Wraps a HuggingFace pipeline object to log its inputs and outputs.

        This method is designed to be used by passing the pipeline object directly.

        :param pipeline_obj: The HuggingFace pipeline object to instrument.
        :type pipeline_obj: Any
        """
        pipeline_id = id(pipeline_obj)
        if pipeline_id in self._instrumented_pipelines:
            print(f"Pipeline {getattr(pipeline_obj, 'model', 'unknown')} already instrumented.")
            return

        print(f"Instrumenting HuggingFace Pipeline: {getattr(pipeline_obj, 'model', 'unknown')}...")

        original_call = pipeline_obj.__call__
        self._instrumented_pipelines[pipeline_id] = original_call

        @functools.wraps(original_call)
        async def wrapper(self_pipeline: Any, inputs: Any, **kwargs: Any) -> List[Dict[str, Any]]:
            session_id = get_current_session_id()
            if not session_id:
                print("Warning: No active LLMTrace session. HuggingFace pipeline call not logged.")
                return await original_call(self_pipeline, inputs, **kwargs)

            model_name = getattr(self_pipeline, 'model', 'unknown_hf_model')

            input_content = inputs if isinstance(inputs, str) else str(inputs)
            await log_message(session_id, "user", input_content, tokens_in=0, tokens_out=0, cost=0, model_name=model_name)

            try:
                results = await original_call(self_pipeline, inputs, **kwargs)
                
                if results and isinstance(results, list) and isinstance(results[0], dict):
                    generated_text = results[0].get("generated_text", "")
                    tokens_info = results[0].get("tokens", {})
                    prompt_tokens = tokens_info.get("prompt", 0)
                    completion_tokens = tokens_info.get("completion", 0)
                    total_tokens = tokens_info.get("total", 0)
                    cost = tokens_info.get("cost", 0.0)

                    await log_message(session_id, "assistant", generated_text,
                                tokens_in=prompt_tokens, tokens_out=completion_tokens, cost=cost, model_name=model_name)
                    await log_metric(session_id, f"huggingface_{model_name}_total_tokens", float(total_tokens))
                    await log_metric(session_id, f"huggingface_{model_name}_cost", cost)
                else:
                    await log_message(session_id, "assistant", str(results), model_name=model_name)
                    await log_error(session_id, "HuggingFace pipeline returned unexpected format.", error_type="DataFormatError")

                return results
            except Exception as e:
                await log_error(session_id, f"HuggingFace pipeline call failed: {e}", details=str(e), error_type="PipelineError")
                raise

        pipeline_obj.__call__ = wrapper.__get__(pipeline_obj, pipeline_obj.__class__)
        print(f"HuggingFace Pipeline {getattr(pipeline_obj, 'model', 'unknown')} instrumentation complete.")

    def uninstrument(self, pipeline_obj: Any) -> None:
        """
        Removes instrumentation from a HuggingFace pipeline object.
        Restores the original `__call__` method if it was previously instrumented.

        :param pipeline_obj: The HuggingFace pipeline object to uninstrument.
        :type pipeline_obj: Any
        """
        pipeline_id = id(pipeline_obj)
        if pipeline_id in self._instrumented_pipelines:
            pipeline_obj.__call__ = self._instrumented_pipelines.pop(pipeline_id)
            print(f"HuggingFace Pipeline {getattr(pipeline_obj, 'model', 'unknown')} uninstrumented.")
        else:
            print(f"Pipeline {getattr(pipeline_obj, 'model', 'unknown')} was not instrumented by this instrumentor.")
