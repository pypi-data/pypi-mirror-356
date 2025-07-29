"""
Instrumentor for OpenAI SDK calls.

This module provides an instrumentor that patches OpenAI's API calls
to automatically capture prompts, responses, token usage, costs, and
log them to the active LLMTrace session.
"""
import functools
from llmtrace.core.core import log_message, log_metric, log_error, get_current_session_id
from llmtrace.tracing.models import Message
from llmtrace.instrumentation.base import BaseInstrumentor
from typing import List, Dict, Any
import asyncio

# --- Mock OpenAI SDK for demonstration purposes ---
class MockOpenAICompletion:
    """
    A mock class simulating OpenAI's ChatCompletion API for testing and demonstration.
    """
    @staticmethod
    async def create(model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Dict[str, Any]:
        """
        Simulates an asynchronous call to OpenAI's ChatCompletion.create.

        :param model: The name of the model being used (e.g., "gpt-4o").
        :type model: str
        :param messages: A list of message dictionaries representing the conversation history.
        :type messages: List[Dict[str, Any]]
        :param kwargs: Additional keyword arguments passed to the OpenAI API.
        :type kwargs: Any
        :returns: A dictionary simulating the OpenAI API response, including choices and usage.
        :rtype: Dict[str, Any]
        """
        print(f"Mock OpenAI: Calling {model} with messages: {messages}")
        await asyncio.sleep(0.05) # Simulate async delay
        prompt_content = messages[0]['content'] if messages and messages[0].get('content') else ""
        response_content = f"This is a mock response to: '{prompt_content[:50]}...'"
        
        prompt_tokens = len(prompt_content.split()) * 1.5
        completion_tokens = len(response_content.split()) * 1.5
        total_tokens = prompt_tokens + completion_tokens
        cost = (total_tokens / 1000) * 0.002 # Example cost per 1k tokens

        return {
            "choices": [{"message": {"role": "assistant", "content": response_content}}],
            "usage": {
                "prompt_tokens": int(prompt_tokens),
                "completion_tokens": int(completion_tokens),
                "total_tokens": int(total_tokens),
            },
            "model": model,
        }

mock_openai = type('OpenAI', (object,), {'ChatCompletion': MockOpenAICompletion})()
# --------------------------------------------------

class OpenAIInstrumentor(BaseInstrumentor):
    """
    Instrumentor for OpenAI SDK calls.

    Patches `openai.ChatCompletion.create` to log prompts and responses
    to the active LLMTrace session.
    """
    def __init__(self):
        """
        Initializes the OpenAIInstrumentor.
        Stores a reference to the original `create` method to allow uninstrumentation.
        """
        self._original_create: Optional[Callable[..., Any]] = None

    def instrument(self) -> None:
        """
        Begins intercepting calls to `openai.ChatCompletion.create`.

        Stores the original method and replaces it with a wrapper that logs
        LLM interactions (prompts, responses, tokens, cost) to the current
        LLMTrace session.
        """
        if self._original_create is not None:
            print("OpenAI already instrumented.")
            return

        print("Instrumenting OpenAI...")
        self._original_create = mock_openai.ChatCompletion.create
        
        @functools.wraps(self._original_create)
        async def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
            session_id = get_current_session_id()
            if not session_id:
                print("Warning: No active LLMTrace session. OpenAI call not logged.")
                return await self._original_create(*args, **kwargs)

            model = kwargs.get('model', 'unknown_model')
            messages = kwargs.get('messages', [])
            
            prompt_content = messages[0]['content'] if messages and messages[0].get('content') else ""
            await log_message(session_id, "user", prompt_content, tokens_in=0, tokens_out=0, cost=0, model_name=model)

            try:
                response = await self._original_create(*args, **kwargs)
                
                response_message = response['choices'][0]['message']
                response_content = response_message['content']
                usage = response.get('usage', {})
                prompt_tokens = usage.get('prompt_tokens', 0)
                completion_tokens = usage.get('completion_tokens', 0)
                total_tokens = usage.get('total_tokens', 0)
                
                # Example cost calculation
                cost = (prompt_tokens / 1000 * 0.002) + (completion_tokens / 1000 * 0.004)

                await log_message(session_id, "assistant", response_content,
                                tokens_in=prompt_tokens, tokens_out=completion_tokens, cost=cost, model_name=model)
                await log_metric(session_id, "openai_total_tokens", float(total_tokens))
                await log_metric(session_id, "openai_cost", cost)

                return response
            except Exception as e:
                await log_error(session_id, f"OpenAI call failed: {e}", details=str(e), error_type="APIError")
                raise

        mock_openai.ChatCompletion.create = wrapper
        print("OpenAI instrumentation complete.")

    def uninstrument(self) -> None:
        """
        Stops intercepting calls to `openai.ChatCompletion.create`.
        Restores the original method if it was previously instrumented.
        """
        if self._original_create is not None:
            mock_openai.ChatCompletion.create = self._original_create
            self._original_create = None
            print("OpenAI uninstrumented.")
