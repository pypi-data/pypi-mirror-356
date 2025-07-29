"""
Abstract base classes for LLMTrace instrumentors.

This module defines the fundamental interface that all LLMTrace instrumentors
must implement to provide consistent instrumentation capabilities across
different LLM frameworks and libraries.
"""

from abc import ABC, abstractmethod
from typing import Any

class BaseInstrumentor(ABC):
    """
    Abstract base class for all LLMTrace instrumentors.

    All concrete instrumentors (e.g., for OpenAI, HuggingFace, LangChain)
    must inherit from this class and implement its abstract methods.
    """

    @abstractmethod
    def instrument(self, *args: Any, **kwargs: Any) -> None:
        """
        Starts the instrumentation process.

        This method should contain the logic to patch or hook into the target
        library's functions or classes to capture LLM interactions.

        :param args: Positional arguments for instrumentation (if any).
        :type args: Any
        :param kwargs: Keyword arguments for instrumentation (if any).
        :type kwargs: Any
        """
        pass

    @abstractmethod
    def uninstrument(self, *args: Any, **kwargs: Any) -> None:
        """
        Stops the instrumentation process.

        This method should revert any changes made by the `instrument` method,
        restoring the original behavior of the target library.

        :param args: Positional arguments for uninstrumentation (if any).
        :type args: Any
        :param kwargs: Keyword arguments for uninstrumentation (if any).
        :type kwargs: Any
        """
        pass
