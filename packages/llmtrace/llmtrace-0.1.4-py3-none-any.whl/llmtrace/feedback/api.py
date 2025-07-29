"""
Public API for recording user feedback within LLMTrace sessions.

This module provides a high-level function to easily capture and log
user feedback associated with LLM interactions, integrating with the
core tracing system.
"""
from llmtrace.core.core import add_feedback
from typing import Optional

async def record_user_feedback(
    session_id: int,
    score: int,
    message_id: Optional[int] = None,
    comment: Optional[str] = None,
    feedback_type: str = "rating"
) -> None:
    """
    Records user feedback for a specific session or message.

    This function acts as the public API for capturing feedback,
    allowing applications to integrate user ratings, thumbs up/down,
    or custom feedback types directly into their LLMTrace logs.

    :param session_id: The ID of the session the feedback belongs to.
    :type session_id: int
    :param score: The numerical score (e.g., 1-5 for rating, or 0/1 for thumbs up/down).
    :type score: int
    :param message_id: The ID of the specific message the feedback is for. Defaults to None.
    :type message_id: Optional[int]
    :param comment: An optional text comment for the feedback. Defaults to None.
    :type comment: Optional[str]
    :param feedback_type: The type of feedback ('rating', 'thumb_up', 'thumb_down', etc.). Defaults to "rating".
    :type feedback_type: str
    """
    if not session_id:
        print("Warning: Cannot record feedback without an active session ID.")
        return

    await add_feedback(session_id, score, message_id, comment, feedback_type)
    print(f"Feedback recorded for session {session_id}, message {message_id if message_id else 'N/A'}: Score={score}, Type={feedback_type}")
