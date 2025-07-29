"""
Defines abstract base classes for storage backends, allowing LLMTrace
to support various database systems beyond SQLite.

This module establishes a common interface for all storage implementations,
ensuring that LLMTrace can interact with different databases (e.g., SQLite, PostgreSQL)
in a consistent and asynchronous manner.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from llmtrace.tracing.models import Session, Message, Metric, Feedback, Error

class StorageBackend(ABC):
    """
    Abstract base class for LLMTrace storage backends.

    All concrete storage implementations must inherit from this class
    and implement its abstract methods to provide database connectivity
    and CRUD operations for tracing data.
    """

    @abstractmethod
    async def connect(self) -> None:
        """
        Establishes an asynchronous connection to the storage backend.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Closes the asynchronous connection to the storage backend.
        """
        pass

    @abstractmethod
    async def create_tables(self) -> None:
        """
        Creates necessary tables/collections in the storage backend if they do not already exist.
        This method is typically called during initialization or migration.
        """
        pass

    @abstractmethod
    async def insert_session(self, session: Session) -> int:
        """
        Inserts a new session record into the storage backend.

        :param session: The Session object to insert.
        :type session: Session
        :returns: The ID of the newly inserted session.
        :rtype: int
        """
        pass

    @abstractmethod
    async def update_session(self, session: Session) -> None:
        """
        Updates an existing session record in the storage backend.

        :param session: The Session object with updated values.
        :type session: Session
        """
        pass

    @abstractmethod
    async def insert_message(self, message: Message) -> int:
        """
        Inserts a new message record into the storage backend.

        :param message: The Message object to insert.
        :type message: Message
        :returns: The ID of the newly inserted message.
        :rtype: int
        """
        pass

    @abstractmethod
    async def insert_metric(self, metric: Metric) -> None:
        """
        Inserts a new metric record into the storage backend.

        :param metric: The Metric object to insert.
        :type metric: Metric
        """
        pass

    @abstractmethod
    async def insert_feedback(self, feedback: Feedback) -> None:
        """
        Inserts new feedback record into the storage backend.

        :param feedback: The Feedback object to insert.
        :type feedback: Feedback
        """
        pass

    @abstractmethod
    async def insert_error(self, error: Error) -> None:
        """
        Inserts a new error record into the storage backend.

        :param error: The Error object to insert.
        :type error: Error
        """
        pass

    @abstractmethod
    async def get_session(self, session_id: int) -> Optional[Session]:
        """
        Retrieves a single session record by its ID.

        :param session_id: The ID of the session to retrieve.
        :type session_id: int
        :returns: The Session object if found, otherwise None.
        :rtype: Optional[Session]
        """
        pass

    @abstractmethod
    async def get_messages_for_session(self, session_id: int) -> List[Message]:
        """
        Retrieves all message records for a given session ID, ordered by timestamp.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Message objects.
        :rtype: List[Message]
        """
        pass

    @abstractmethod
    async def get_all_sessions(self) -> List[Session]:
        """
        Retrieves all session records from the storage backend, ordered by start time descending.

        :returns: A list of Session objects.
        :rtype: List[Session]
        """
        pass

    @abstractmethod
    async def get_metrics_for_session(self, session_id: int) -> List[Metric]:
        """
        Retrieves all metric records for a given session ID, ordered by timestamp.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Metric objects.
        :rtype: List[Metric]
        """
        pass

    @abstractmethod
    async def get_feedback_for_session(self, session_id: int) -> List[Feedback]:
        """
        Retrieves all feedback entries for a given session ID, ordered by timestamp.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Feedback objects.
        :rtype: List[Feedback]
        """
        pass

    @abstractmethod
    async def get_errors_for_session(self, session_id: int) -> List[Error]:
        """
        Retrieves all error entries for a given session ID, ordered by timestamp.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Error objects.
        :rtype: List[Error]
        """
        pass

    @abstractmethod
    async def get_filtered_sessions(self, start_time: Optional[str] = None, end_time: Optional[str] = None,
                             session_name: Optional[str] = None, user_id: Optional[str] = None,
                             message_content_search: Optional[str] = None, model_name: Optional[str] = None,
                             min_tokens: Optional[int] = None, max_tokens: Optional[int] = None,
                             min_cost: Optional[float] = None, max_cost: Optional[float] = None) -> List[Session]:
        """
        Retrieves session records based on various filter criteria.

        :param start_time: Filter sessions starting after this time (ISO format).
        :type start_time: Optional[str]
        :param end_time: Filter sessions ending before this time (ISO format).
        :type end_time: Optional[str]
        :param session_name: Filter sessions by name (partial match).
        :type session_name: Optional[str]
        :param user_id: Filter sessions by user ID (partial match).
        :type user_id: Optional[str]
        :param message_content_search: Filter sessions by content in their messages (partial match).
        :type message_content_search: Optional[str]
        :param model_name: Filter sessions by model name used in messages (partial match).
        :type model_name: Optional[str]
        :param min_tokens: Filter sessions with total_tokens greater than or equal to this value.
        :type min_tokens: Optional[int]
        :param max_tokens: Filter sessions with total_tokens less than or equal to this value.
        :type max_tokens: Optional[int]
        :param min_cost: Filter sessions with total_cost greater than or equal to this value.
        :type min_cost: Optional[float]
        :param max_cost: Filter sessions with total_cost less than or equal to this value.
        :type max_cost: Optional[float]
        :returns: A list of filtered Session objects.
        :rtype: List[Session]
        """
        pass

    @abstractmethod
    async def delete_session(self, session_id: int) -> None:
        """
        Deletes a session record and its associated data (messages, metrics, feedback, errors).
        Requires ON DELETE CASCADE on foreign keys in table creation for relational databases.

        :param session_id: The ID of the session to delete.
        :type session_id: int
        """
        pass

    @abstractmethod
    async def get_overall_metrics_summary(self) -> Dict[str, Any]:
        """
        Retrieves overall aggregated metrics and statistics across all sessions.

        :returns: A dictionary containing various aggregated metrics (e.g., total sessions, total tokens, error rate).
        :rtype: Dict[str, Any]
        """
        pass

    @abstractmethod
    async def get_metrics_time_series(self, metric_name: str, interval: str,
                                      start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves time-series data for a specific metric.

        :param metric_name: The name of the metric.
        :type metric_name: str
        :param interval: The time aggregation interval ('hour', 'day').
        :type interval: str
        :param start_date: Filter data starting after this date (YYYY-MM-DD).
        :type start_date: Optional[str]
        :param end_date: Filter data ending before this date (YYYY-MM-DD).
        :type end_date: Optional[str]
        :returns: A list of dictionaries with time buckets and aggregated values.
        :rtype: List[Dict[str, Any]]
        """
        pass

    @abstractmethod
    async def get_model_token_usage(self) -> List[Dict[str, Any]]:
        """
        Retrieves aggregated token usage per model across all messages.

        :returns: A list of dictionaries with model names and their total token usage.
        :rtype: List[Dict[str, Any]]
        """
        pass

    @abstractmethod
    async def get_feedback_score_distribution(self) -> List[Dict[str, Any]]:
        """
        Retrieves the distribution of feedback scores (for 'rating' type feedback).

        :returns: A list of dictionaries, each with a 'score' and its 'count'.
        :rtype: List[Dict[str, Any]]
        """
        pass

    @abstractmethod
    async def get_error_type_counts(self) -> List[Dict[str, Any]]:
        """
        Retrieves the counts of different error types recorded.

        :returns: A list of dictionaries, each with an 'error_type' and its 'count'.
        :rtype: List[Dict[str, Any]]
        """
        pass

    @abstractmethod
    async def get_avg_session_duration(self) -> float:
        """
        Retrieves the average duration of completed sessions in seconds.

        :returns: The average session duration in seconds. Returns 0.0 if no completed sessions.
        :rtype: float
        """
        pass
