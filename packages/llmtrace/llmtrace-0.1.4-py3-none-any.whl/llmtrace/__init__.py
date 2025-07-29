"""
LLMTrace: framework ligero de observabilidad y evaluación para aplicaciones con LLMs.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# --------------------------------------------------------------------------- #
# Configuración de logging
# --------------------------------------------------------------------------- #
from llmtrace._logging import setup_logger

_log_format = os.getenv("LLMTRACE_LOG_FORMAT", "text").lower()
setup_logger(json_format=_log_format == "json")

# --------------------------------------------------------------------------- #
# API pública de alto nivel
# --------------------------------------------------------------------------- #
from llmtrace.core.core import (  # noqa: F401
    init,
    session,
    get_current_session_id,
    log_message,
    log_metric,
    add_feedback,
    log_error,
    get_sessions,
    get_messages,
    get_metrics,
    get_feedback,
    get_errors,
)
from llmtrace.instrumentation.base import BaseInstrumentor  # noqa: F401
from llmtrace.instrumentation.openai import OpenAIInstrumentor  # noqa: F401
from llmtrace.instrumentation.huggingface import HFInstrumentor  # noqa: F401

# LangChain es opcional: sólo se expone si el usuario instaló langchain-core
try:
    from llmtrace.instrumentation.langchain import (  # noqa: F401
        LangChainCallbackHandler,
    )
except ImportError:  # pragma: no cover
    LangChainCallbackHandler = None  # type: ignore

from llmtrace.storage.backends import StorageBackend  # noqa: F401
from llmtrace.tracing.models import (  # noqa: F401
    Session,
    Message,
    Metric,
    Feedback,
    Error,
)

# --------------------------------------------------------------------------- #
# Utilidades
# --------------------------------------------------------------------------- #
async def close() -> None:
    """
    Cierra la conexión activa a la base de datos de LLMTrace.
    """
    import logging
    from llmtrace.core.core import _db_instance

    logger = logging.getLogger("llmtrace")
    if _db_instance:
        await _db_instance.close()
        logger.info("LLMTrace database connection closed.")
    else:
        logger.warning("LLMTrace was not initialized or already closed.")

# --------------------------------------------------------------------------- #
# Versión del paquete (rellenada por setuptools_scm)
# --------------------------------------------------------------------------- #
try:
    from ._version import version as __version__  # type: ignore
except ImportError:  # pragma: no cover
    __version__ = "0.0.0+unknown"
