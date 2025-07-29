"""
LangChain Callback Handler for LLMTrace.

This module provides a custom LangChain callback handler that integrates
with LLMTrace's core system to log LLM events (prompts, responses, errors,
and associated metrics) from LangChain applications.
"""
from llmtrace.core.core import log_message, log_metric, log_error, get_current_session_id
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from typing import Any, Dict, List, Union, Optional
import uuid
from llmtrace.instrumentation.base import BaseInstrumentor

class LangChainCallbackHandler(BaseInstrumentor, BaseCallbackHandler):
    """
    LangChain Callback Handler for LLMTrace.

    Logs LLM calls, prompts, responses, and metrics to the current LLMTrace session.
    This class acts as both a LangChain callback and an LLMTrace instrumentor,
    allowing seamless integration with LangChain's callback system.
    """
    def __init__(self):
        """
        Initializes the LangChainCallbackHandler.
        """
        super().__init__()
        self.current_run_id: Optional[str] = None

    def instrument(self) -> None:
        """
        This method is a placeholder for BaseInstrumentor.

        LangChain instrumentation is activated by passing an instance of this handler
        to the LangChain LLM or Chain's `callbacks` parameter.
        """
        print("LangChain instrumentation is activated by passing an instance of LangChainCallbackHandler to your LangChain LLM/Chain's `callbacks` parameter.")

    def uninstrument(self) -> None:
        """
        This method is a placeholder for BaseInstrumentor.

        To stop LangChain instrumentation, simply stop passing this handler
        to your LangChain LLM or Chain.
        """
        print("LangChain instrumentation is stopped by no longer passing an instance of LangChainCallbackHandler to your LangChain LLM/Chain's `callbacks` parameter.")

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """
        Run when an LLM starts running. Logs the prompt message(s).

        :param serialized: The serialized LLM object.
        :type serialized: Dict[str, Any]
        :param prompts: The list of prompt strings sent to the LLM.
        :type prompts: List[str]
        :param kwargs: Additional keyword arguments, including `run_id`.
        :type kwargs: Any
        """
        session_id = get_current_session_id()
        if not session_id:
            print("Warning: No active LLMTrace session. LangChain LLM call not logged.")
            return

        self.current_run_id = kwargs.get("run_id", str(uuid.uuid4()))
        model_name = serialized.get("name", serialized.get("id", ["unknown_langchain_model"])[-1])

        for i, prompt in enumerate(prompts):
            await log_message(session_id, "user", prompt, tokens_in=0, tokens_out=0, cost=0, model_name=model_name)
            print(f"LangChain: Logged prompt for run {self.current_run_id}: {prompt[:50]}...")

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """
        Run when an LLM finishes running successfully. Logs the response message and metrics.

        :param response: The LLM response object containing generated text and usage information.
        :type response: LLMResult
        :param kwargs: Additional keyword arguments.
        :type kwargs: Any
        """
        session_id = get_current_session_id()
        if not session_id:
            return

        generated_text = response.generations[0][0].text if response.generations and response.generations[0] else ""
        
        token_usage = response.llm_output.get("token_usage", {}) if response.llm_output else {}
        prompt_tokens = token_usage.get("prompt_tokens", 0)
        completion_tokens = token_usage.get("completion_tokens", 0)
        total_tokens = token_usage.get("total_tokens", 0)
        model_name = response.llm_output.get("model_name", "unknown_langchain_model") if response.llm_output else "unknown_langchain_model"
        
        # Example cost calculation (LangChain might not provide cost directly)
        cost = (prompt_tokens / 1000 * 0.002) + (completion_tokens / 1000 * 0.004)

        await log_message(session_id, "assistant", generated_text,
                    tokens_in=prompt_tokens, tokens_out=completion_tokens, cost=cost, model_name=model_name)
        await log_metric(session_id, f"langchain_{model_name}_total_tokens", float(total_tokens))
        await log_metric(session_id, f"langchain_{model_name}_cost", cost)
        print(f"LangChain: Logged response for run {self.current_run_id}: {generated_text[:50]}...")

    async def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """
        Run when an LLM errors during execution. Logs the error details.

        :param error: The exception or KeyboardInterrupt that occurred.
        :type error: Union[Exception, KeyboardInterrupt]
        :param kwargs: Additional keyword arguments.
        :type kwargs: Any
        """
        session_id = get_current_session_id()
        if not session_id:
            return
        await log_error(session_id, f"LangChain LLM Error: {error}", details=str(error), error_type="LangChainError")
        print(f"LangChain: Logged error for run {self.current_run_id}: {error}")
