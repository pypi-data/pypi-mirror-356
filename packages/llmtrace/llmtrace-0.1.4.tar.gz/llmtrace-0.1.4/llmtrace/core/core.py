"""
Core functionalities for LLMTrace, including initialization, session management,
and logging of LLM interactions, metrics, feedback, and errors.

This module provides the central API for interacting with the LLMTrace system,
allowing users to define tracing sessions and log various events associated
with Large Language Model (LLM) applications.
"""

import logging
from llmtrace.storage import get_storage_backend
from llmtrace.tracing.models import Session, Message, Metric, Feedback, Error
from datetime import datetime
import asyncio
from asyncio import Lock
from contextlib import asynccontextmanager
from typing import Optional, List, ContextManager, TYPE_CHECKING

if TYPE_CHECKING:
    from llmtrace.storage.backends import StorageBackend

logger = logging.getLogger("llmtrace.core") # Usar el logger configurado

_db_instance: Optional["StorageBackend"] = None
_current_session_id: Optional[int] = None
_session_lock = Lock()
_app_name: Optional[str] = None

async def init(db_path: str = '~/.llmtrace/llmtrace.db', app_name: Optional[str] = None, backend_type: Optional[str] = None, **backend_kwargs):
    """
    Initializes the LLMTrace database connection and global configuration.
    Must be called once at the start of your application.

    :param db_path: Path to the SQLite database file. Defaults to '~/.llmtrace/llmtrace.db'.
                    Admite 'memory://' para una base de datos en memoria (útil para tests).
    :type db_path: str
    :param app_name: An optional name for your application, used for identification.
    :type app_name: Optional[str]
    :param backend_type: The type of storage backend to use ('sqlite', 'postgresql').
                         Defaults to 'sqlite' if not specified or via env var.
    :type backend_type: Optional[str]
    :param backend_kwargs: Additional keyword arguments to pass to the backend constructor.
    :type backend_kwargs: Any
    :raises RuntimeError: If LLMTrace is already initialized.
    """
    global _db_instance, _app_name
    if _db_instance is None:
        _db_instance = await get_storage_backend(backend_type=backend_type, db_path=db_path, **backend_kwargs)
        _app_name = app_name
        logger.info(f"LLMTrace initialized. Database at: {_db_instance.db_path}, App Name: {_app_name}")
    else:
        logger.warning("LLMTrace already initialized.")

@asynccontextmanager
async def session(name: Optional[str] = None, user_id: Optional[str] = None):
    """
    Asynchronous context manager for defining a tracing session.
    All LLM calls logged within this context will be associated with this session.

    Usage::

        async with llmtrace.session(name="My Chat", user_id="user_123") as session_id:
            # Perform LLM interactions here
            await llmtrace.log_message(session_id, "user", "Hello!")

    :param name: An optional name for the session.
    :type name: Optional[str]
    :param user_id: An optional user ID associated with the session.
    :type user_id: Optional[str]
    :yields: The ID of the newly created session.
    :rtype: int
    :raises RuntimeError: If LLMTrace has not been initialized.
    """
    global _current_session_id
    if _db_instance is None:
        raise RuntimeError("LLMTrace not initialized. Call llmtrace.init() first.")

    previous_session_id: Optional[int] = None
    session_id: Optional[int] = None

    async with _session_lock:
        previous_session_id = _current_session_id
        new_session = Session(name=name, start_time=datetime.now(), user_id=user_id)
        session_id = await _db_instance.insert_session(new_session)
        _current_session_id = session_id
        logger.info(f"LLMTrace session '{name}' created: {session_id}")
    
    try:
        yield session_id
    finally:
        async with _session_lock:
            if session_id is not None:
                session_obj = await _db_instance.get_session(session_id)
                if session_obj:
                    session_obj.end_time = datetime.now()
                    messages = await _db_instance.get_messages_for_session(session_id)
                    session_obj.total_tokens = sum(m.tokens_in + m.tokens_out for m in messages)
                    session_obj.total_cost = sum(m.cost for m in messages)
                    await _db_instance.update_session(session_obj)
                    logger.info(f"LLMTrace session {session_id} ended.")
                else:
                    logger.warning(f"Session {session_id} not found. Cannot end.")
            
            _current_session_id = previous_session_id

def get_current_session_id() -> Optional[int]:
    """
    Returns the ID of the current active tracing session.

    This function is useful for instrumentors or other parts of your application
    that need to associate events with the ongoing session without explicitly
    passing the session ID around.

    :returns: The current session ID, or None if no session is active.
    :rtype: Optional[int]
    """
    return _current_session_id

async def log_message(session_id: int, role: str, content: str, tokens_in: int = 0, tokens_out: int = 0, cost: float = 0.0, model_name: Optional[str] = None):
    """
    Logs a message (prompt or response) to the specified session.

    This function is typically called by instrumentors to record LLM inputs and outputs.

    :param session_id: The ID of the session to log the message to.
    :type session_id: int
    :param role: The role of the message ('user', 'assistant', 'system', 'tool').
    :type role: str
    :param content: The text content of the message.
    :type content: str
    :param tokens_in: Number of input tokens for the message. Defaults to 0.
    :type tokens_in: int
    :param tokens_out: Number of output tokens for the message. Defaults to 0.
    :type tokens_out: int
    :param cost: Estimated cost of the message. Defaults to 0.0.
    :type cost: float
    :param model_name: The name of the LLM model used for this message. Defaults to None.
    :type model_name: Optional[str]
    :returns: The ID of the newly inserted message, or None if not logged due to uninitialized LLMTrace.
    :rtype: Optional[int]
    """
    if _db_instance is None:
        logger.warning("LLMTrace not initialized. Message not logged.")
        return None
    
    message = Message(
        session_id=session_id,
        role=role,
        content=content,
        timestamp=datetime.now(),
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        cost=cost,
        model_name=model_name
    )
    message_id = await _db_instance.insert_message(message)
    logger.debug(f"Logged message for session {session_id}: {message.role} - {message.content[:50]}...")
    return message_id

async def log_metric(session_id: int, name: str, value: float):
    """
    Logs a custom metric for the specified session.

    Metrics can represent various quantitative aspects of an LLM interaction,
    such as latency, response quality scores, or custom evaluation results.

    :param session_id: The ID of the session to log the metric to.
    :type session_id: int
    :param name: The name of the metric (e.g., 'latency_ms', 'response_quality').
    :type name: str
    :param value: The numerical value of the metric.
    :type value: float
    """
    if _db_instance is None:
        logger.warning("LLMTrace not initialized. Metric not logged.")
        return
    
    metric = Metric(
        session_id=session_id,
        name=name,
        value=value,
        timestamp=datetime.now()
    )
    await _db_instance.insert_metric(metric)
    logger.debug(f"Logged metric for session {session_id}: {metric.name}={metric.value}")

async def add_feedback(session_id: int, score: int, message_id: Optional[int] = None, comment: Optional[str] = None, feedback_type: str = "rating"):
    """
    Logs user feedback for a specific message or session.
    This is the public API for capturing feedback.

    Feedback can be used to capture user satisfaction, relevance, or other qualitative
    assessments of LLM responses.

    :param session_id: The ID of the session the feedback belongs to.
    :type session_id: int
    :param score: The numerical score of the feedback (e.g., 1-5 for rating, 0/1 for thumbs up/down).
    :type score: int
    :param message_id: The ID of the specific message the feedback is for. Defaults to None (session-level feedback).
    :type message_id: Optional[int]
    :param comment: An optional text comment for the feedback. Defaults to None.
    :type comment: Optional[str]
    :param feedback_type: The type of feedback ('rating', 'thumb_up', 'thumb_down', etc.). Defaults to "rating".
    :type feedback_type: str
    """
    if _db_instance is None:
        logger.warning("LLMTrace not initialized. Feedback not logged.")
        return
    
    feedback = Feedback(
        session_id=session_id,
        message_id=message_id,
        type=feedback_type,
        score=score,
        comment=comment,
        timestamp=datetime.now()
    )
    await _db_instance.insert_feedback(feedback)
    logger.info(f"Logged feedback for session {session_id}, message {message_id}: Type={feedback_type}, Score={score}")

async def log_error(session_id: int, message: str, details: Optional[str] = None, message_id: Optional[int] = None, error_type: Optional[str] = None):
    """
    Logs an error associated with the specified session or message.

    This function helps in tracking and debugging issues that occur during LLM interactions.

    :param session_id: The ID of the session the error belongs to.
    :type session_id: int
    :param message: A brief description of the error.
    :type message: str
    :param details: More detailed information about the error (e.g., stack trace). Defaults to None.
    :type details: Optional[str]
    :param message_id: The ID of the specific message related to the error. Defaults to None.
    :type message_id: Optional[int]
    :param error_type: The type of error (e.g., 'APIError', 'NetworkError', 'ValueError'). Defaults to None.
    :type error_type: Optional[str]
    """
    if _db_instance is None:
        logger.warning("LLMTrace not initialized. Error not logged.")
        return
    
    error = Error(
        session_id=session_id,
        message_id=message_id,
        error_type=error_type,
        message=message,
        timestamp=datetime.now(),
        details=details
    )
    await _db_instance.insert_error(error)
    logger.error(f"Logged error for session {session_id}: {message}")

async def get_sessions() -> List[Session]:
    """
    Returns a list of all tracing sessions, ordered by start time descending.

    This function provides a programmatic way to retrieve all recorded sessions.

    :returns: A list of Session objects.
    :rtype: List[Session]
    """
    if _db_instance is None:
        logger.warning("LLMTrace not initialized. Cannot retrieve sessions.")
        return []
    return await _db_instance.get_all_sessions()

async def get_messages(session_id: int) -> List[Message]:
    """
    Returns a list of messages for a given session ID, ordered by timestamp ascending.

    This function allows retrieval of the full conversation history for a specific session.

    :param session_id: The ID of the session to retrieve messages for.
    :type session_id: int
    :returns: A list of Message objects.
    :rtype: List[Message]
    """
    if _db_instance is None:
        logger.warning("LLMTrace not initialized. Cannot retrieve messages.")
        return []
    return await _db_instance.get_messages_for_session(session_id)

async def get_metrics(session_id: int) -> List[Metric]:
    """
    Returns a list of metrics for a given session ID, ordered by timestamp ascending.

    This function provides access to custom evaluation results and performance indicators
    associated with a session.

    :param session_id: The ID of the session to retrieve metrics for.
    :type session_id: int
    :returns: A list of Metric objects.
    :rtype: List[Metric]
    """
    if _db_instance is None:
        logger.warning("LLMTrace not initialized. Cannot retrieve metrics.")
        return []
    return await _db_instance.get_metrics_for_session(session_id)

async def get_feedback(session_id: int) -> List[Feedback]:
    """
    Returns a list of feedback entries for a given session ID, ordered by timestamp ascending.

    This function allows retrieval of user feedback provided for a specific session.

    :param session_id: The ID of the session to retrieve feedback for.
    :type session_id: int
    :returns: A list of Feedback objects.
    :rtype: List[Feedback]
    """
    if _db_instance is None:
        logger.warning("LLMTrace not initialized. Cannot retrieve feedback.")
        return []
    return await _db_instance.get_feedback_for_session(session_id)

async def get_errors(session_id: int) -> List[Error]:
    """
    Returns a list of errors for a given session ID, ordered by timestamp ascending.

    This function provides access to error logs associated with a specific session.

    :param session_id: The ID of the session to retrieve errors for.
    :type session_id: int
    :returns: A list of Error objects.
    :rtype: List[Error]
    """
    if _db_instance is None:
        logger.warning("LLMTrace not initialized. Cannot retrieve errors.")
        return []
    return await _db_instance.get_errors_for_session(session_id)
