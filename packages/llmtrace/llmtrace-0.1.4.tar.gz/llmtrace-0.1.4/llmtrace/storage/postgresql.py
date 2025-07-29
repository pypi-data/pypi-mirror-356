"""
PostgreSQL backend implementation for LLMTrace.

This module provides a concrete implementation of the :class:`llmtrace.storage.backends.StorageBackend`
abstract interface using `asyncpg` for asynchronous PostgreSQL database operations.
It handles database connection, table creation, and CRUD operations for tracing data,
including content compression.
"""
import asyncpg
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
import zlib

from llmtrace.tracing.models import Session, Message, Metric, Feedback, Error
from llmtrace.storage.backends import StorageBackend

class PostgreSQLBackend(StorageBackend):
    """
    PostgreSQL backend for LLMTrace.

    Implements the :class:`llmtrace.storage.backends.StorageBackend` abstract interface.
    Connects to a PostgreSQL database using the provided connection string.
    """
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initializes the PostgreSQLBackend.

        :param connection_string: The PostgreSQL connection string.
                                  Defaults to reading from PG_CONNECTION_STRING env var if None.
        :type connection_string: Optional[str]
        :raises ValueError: If the PostgreSQL connection string is not provided and the environment variable is not set.
        """
        self.connection_string = connection_string or os.getenv("PG_CONNECTION_STRING")
        if not self.connection_string:
            raise ValueError("PostgreSQL connection string not provided and PG_CONNECTION_STRING env var not set.")
        self._connection: Optional[asyncpg.Connection] = None

    async def connect(self) -> None:
        """
        Establishes an asynchronous connection to the PostgreSQL database.

        If the connection is already established or closed, it attempts to reconnect.
        Also calls `create_tables()` to ensure the schema is present.

        :raises asyncpg.exceptions.PostgresError: If there is an error connecting to the database.
        """
        if self._connection is None or self._connection.is_closed():
            try:
                self._connection = await asyncpg.connect(self.connection_string)
                print("Connected to PostgreSQL.")
                await self.create_tables()
            except asyncpg.exceptions.PostgresError as e:
                print(f"Error connecting to PostgreSQL: {e}")
                raise

    async def close(self) -> None:
        """
        Closes the asynchronous connection to the PostgreSQL database.
        """
        if self._connection and not self._connection.is_closed():
            await self._connection.close()
            self._connection = None
            print("Disconnected from PostgreSQL.")

    async def _execute(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False) -> Any:
        """
        Executes an asynchronous SQL query and optionally fetches results.

        This is an internal helper method to abstract common database operations.

        :param query: The SQL query string.
        :type query: str
        :param params: Parameters to substitute into the query. Defaults to an empty tuple.
        :type params: tuple
        :param fetch_one: If True, fetches one row after execution. Defaults to False.
        :type fetch_one: bool
        :param fetch_all: If True, fetches all rows after execution. Defaults to False.
        :type fetch_all: bool
        :returns: Fetched row(s) (asyncpg.Record or list of asyncpg.Record) or None for non-fetch operations.
        :rtype: Any
        :raises asyncpg.exceptions.PostgresError: If there is an error executing the query.
        """
        await self.connect()
        try:
            if fetch_one:
                return await self._connection.fetchrow(query, *params)
            if fetch_all:
                return await self._connection.fetch(query, *params)
            await self._connection.execute(query, *params)
            return None
        except asyncpg.exceptions.PostgresError as e:
            print(f"Error executing query: {e}")
            raise

    async def create_tables(self) -> None:
        """
        Creates necessary tables in the PostgreSQL database if they do not already exist.
        """
        queries = [
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id SERIAL PRIMARY KEY,
                name TEXT,
                start_time TIMESTAMP WITH TIME ZONE NOT NULL,
                end_time TIMESTAMP WITH TIME ZONE,
                total_tokens INTEGER DEFAULT 0,
                total_cost DOUBLE PRECISION DEFAULT 0.0,
                user_id TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content BYTEA NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                tokens_in INTEGER DEFAULT 0,
                tokens_out INTEGER DEFAULT 0,
                cost DOUBLE PRECISION DEFAULT 0.0,
                model_name TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS metrics (
                id SERIAL PRIMARY KEY,
                session_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                value DOUBLE PRECISION NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                session_id INTEGER NOT NULL,
                message_id INTEGER,
                type TEXT NOT NULL,
                score INTEGER,
                comment TEXT,
                timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS errors (
                id SERIAL PRIMARY KEY,
                session_id INTEGER NOT NULL,
                message_id INTEGER,
                error_type TEXT,
                message TEXT NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                details TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
            );
            """
        ]
        for query in queries:
            await self._execute(query)
        print("PostgreSQL tables ensured.")

    async def insert_session(self, session: Session) -> int:
        """
        Inserts a new session into the database.

        :param session: The Session object to insert.
        :type session: Session
        :returns: The ID of the newly inserted session.
        :rtype: int
        """
        row = await self._execute(
            "INSERT INTO sessions (name, start_time, user_id) VALUES ($1, $2, $3) RETURNING id;",
            (session.name, session.start_time, session.user_id),
            fetch_one=True
        )
        session.id = row['id']
        return session.id

    async def update_session(self, session: Session) -> None:
        """
        Updates an existing session in the database.

        :param session: The Session object with updated values.
        :type session: Session
        """
        await self._execute(
            """
            UPDATE sessions SET name = $1, end_time = $2, total_tokens = $3, total_cost = $4, user_id = $5
            WHERE id = $6;
            """,
            (session.name, session.end_time, session.total_tokens, session.total_cost, session.user_id, session.id)
        )

    async def insert_message(self, message: Message) -> int:
        """
        Inserts a new message into the database. Message content is compressed before storage.

        :param message: The Message object to insert.
        :type message: Message
        :returns: The ID of the newly inserted message.
        :rtype: int
        """
        compressed_content = zlib.compress(message.content.encode('utf-8'))
        row = await self._execute(
            """
            INSERT INTO messages (session_id, role, content, timestamp, tokens_in, tokens_out, cost, model_name)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id;
            """,
            (message.session_id, message.role, compressed_content, message.timestamp,
             message.tokens_in, message.tokens_out, message.cost, message.model_name),
            fetch_one=True
        )
        message.id = row['id']
        return message.id

    async def insert_metric(self, metric: Metric) -> None:
        """
        Inserts a new metric into the database.

        :param metric: The Metric object to insert.
        :type metric: Metric
        """
        await self._execute(
            "INSERT INTO metrics (session_id, name, value, timestamp) VALUES ($1, $2, $3, $4);",
            (metric.session_id, metric.name, metric.value, metric.timestamp)
        )

    async def insert_feedback(self, feedback: Feedback) -> None:
        """
        Inserts new feedback into the database.

        :param feedback: The Feedback object to insert.
        :type feedback: Feedback
        """
        await self._execute(
            "INSERT INTO feedback (session_id, message_id, type, score, comment, timestamp) VALUES ($1, $2, $3, $4, $5, $6);",
            (feedback.session_id, feedback.message_id, feedback.type, feedback.score, feedback.comment, feedback.timestamp)
        )

    async def insert_error(self, error: Error) -> None:
        """
        Inserts a new error into the database.

        :param error: The Error object to insert.
        :type error: Error
        """
        await self._execute(
            "INSERT INTO errors (session_id, message_id, error_type, message, timestamp, details) VALUES ($1, $2, $3, $4, $5, $6);",
            (error.session_id, error.message_id, error.error_type, error.message, error.timestamp, error.details)
        )

    async def get_session(self, session_id: int) -> Optional[Session]:
        """
        Retrieves a single session by its ID.

        :param session_id: The ID of the session to retrieve.
        :type session_id: int
        :returns: The Session object if found, otherwise None.
        :rtype: Optional[Session]
        """
        row = await self._execute("SELECT * FROM sessions WHERE id = $1;", (session_id,), fetch_one=True)
        return Session.from_db_row(row) if row else None

    async def get_messages_for_session(self, session_id: int) -> List[Message]:
        """
        Retrieves all messages for a given session ID. Message content is decompressed.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Message objects.
        :rtype: List[Message]
        """
        rows = await self._execute("SELECT * FROM messages WHERE session_id = $1 ORDER BY timestamp ASC;", (session_id,), fetch_all=True)
        return [Message.from_db_row(row) for row in rows]

    async def get_all_sessions(self) -> List[Session]:
        """
        Retrieves all sessions from the database, ordered by start time descending.

        :returns: A list of Session objects.
        :rtype: List[Session]
        """
        rows = await self._execute("SELECT * FROM sessions ORDER BY start_time DESC;", fetch_all=True)
        return [Session.from_db_row(row) for row in rows]

    async def get_metrics_for_session(self, session_id: int) -> List[Metric]:
        """
        Retrieves all metrics for a given session ID.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Metric objects.
        :rtype: List[Metric]
        """
        rows = await self._execute("SELECT * FROM metrics WHERE session_id = $1 ORDER BY timestamp ASC;", (session_id,), fetch_all=True)
        return [Metric.from_db_row(row) for row in rows]

    async def get_feedback_for_session(self, session_id: int) -> List[Feedback]:
        """
        Retrieves all feedback entries for a given session ID.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Feedback objects.
        :rtype: List[Feedback]
        """
        rows = await self._execute("SELECT * FROM feedback WHERE session_id = $1 ORDER BY timestamp ASC;", (session_id,), fetch_all=True)
        return [Feedback.from_db_row(row) for row in rows]

    async def get_errors_for_session(self, session_id: int) -> List[Error]:
        """
        Retrieves all error entries for a given session ID.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Error objects.
        :rtype: List[Error]
        """
        rows = await self._execute("SELECT * FROM errors WHERE session_id = $1 ORDER BY timestamp ASC;", (session_id,), fetch_all=True)
        return [Error.from_db_row(row) for row in rows]

    async def get_filtered_sessions(self, start_time: Optional[str] = None, end_time: Optional[str] = None,
                             session_name: Optional[str] = None, user_id: Optional[str] = None,
                             message_content_search: Optional[str] = None, model_name: Optional[str] = None,
                             min_tokens: Optional[int] = None, max_tokens: Optional[int] = None,
                             min_cost: Optional[float] = None, max_cost: Optional[float] = None) -> List[Session]:
        """
        Retrieves sessions based on various filter criteria.

        :param start_time: Filter sessions starting after this time (ISO format).
        :type start_time: Optional[str]
        :param end_time: Filter sessions ending before this time (ISO format).
        :type end_time: Optional[str]
        :param session_name: Filter sessions by name (partial match).
        :type session_name: Optional[str]
        :param user_id: Filter sessions by user ID (partial match).
        :type user_id: Optional[str]
        :param message_content_search: Filter sessions by content in their messages (partial match).
                                      Note: Direct search on compressed BYTEA content is not efficient
                                      in PostgreSQL without full-text search or custom functions.
                                      This filter is currently ignored for PostgreSQL.
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
        query = "SELECT DISTINCT s.* FROM sessions s"
        params = []
        joins = []
        where_clauses = []
        param_counter = 1

        if message_content_search or model_name:
            joins.append("JOIN messages m ON s.id = m.session_id")

        if start_time:
            where_clauses.append(f"s.start_time >= ${param_counter}")
            params.append(start_time)
            param_counter += 1
        if end_time:
            where_clauses.append(f"s.end_time <= ${param_counter}")
            params.append(end_time)
            param_counter += 1
        if session_name:
            where_clauses.append(f"s.name ILIKE ${param_counter}")
            params.append(f"%{session_name}%")
            param_counter += 1
        if user_id:
            where_clauses.append(f"s.user_id ILIKE ${param_counter}")
            params.append(f"%{user_id}%")
            param_counter += 1
        # message_content_search is intentionally skipped here due to BYTEA compression
        if model_name:
            where_clauses.append(f"m.model_name ILIKE ${param_counter}")
            params.append(f"%{model_name}%")
            param_counter += 1
        if min_tokens is not None:
            where_clauses.append(f"s.total_tokens >= ${param_counter}")
            params.append(min_tokens)
            param_counter += 1
        if max_tokens is not None:
            where_clauses.append(f"s.total_tokens <= ${param_counter}")
            params.append(max_tokens)
            param_counter += 1
        if min_cost is not None:
            where_clauses.append(f"s.total_cost >= ${param_counter}")
            params.append(min_cost)
            param_counter += 1
        if max_cost is not None:
            where_clauses.append(f"s.total_cost <= ${param_counter}")
            params.append(max_cost)
            param_counter += 1

        if joins:
            query += " " + " ".join(joins)
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += " ORDER BY s.start_time DESC;"
        
        rows = await self._execute(query, tuple(params), fetch_all=True)
        return [Session.from_db_row(row) for row in rows]

    async def delete_session(self, session_id: int) -> None:
        """
        Deletes a session and all its associated data (messages, metrics, feedback, errors).
        This operation relies on `ON DELETE CASCADE` foreign key constraints defined during table creation.

        :param session_id: The ID of the session to delete.
        :type session_id: int
        """
        await self._execute("DELETE FROM sessions WHERE id = $1;", (session_id,))
        print(f"Session {session_id} and all associated data deleted.")

    async def get_overall_metrics_summary(self) -> Dict[str, Any]:
        """
        Retrieves overall aggregated metrics and statistics across all sessions.

        :returns: A dictionary containing various aggregated metrics such as total sessions,
                  total tokens, total cost, average tokens/cost per session, error rate,
                  average feedback score, top error types, and top models by token usage.
        :rtype: Dict[str, Any]
        """
        summary = {}

        summary["total_sessions"] = (await self._execute("SELECT COUNT(id) FROM sessions;", fetch_one=True))[0]
        summary["total_messages"] = (await self._execute("SELECT COUNT(id) FROM messages;", fetch_one=True))[0]
        summary["total_tokens_overall"] = (await self._execute("SELECT SUM(total_tokens) FROM sessions;", fetch_one=True))[0] or 0
        summary["total_cost_overall"] = (await self._execute("SELECT SUM(total_cost) FROM sessions;", fetch_one=True))[0] or 0.0
        summary["avg_tokens_per_session"] = (await self._execute("SELECT AVG(total_tokens) FROM sessions;", fetch_one=True))[0] or 0.0
        summary["avg_cost_per_session"] = (await self._execute("SELECT AVG(total_cost) FROM sessions;", fetch_one=True))[0] or 0.0

        sessions_with_errors = (await self._execute("SELECT COUNT(DISTINCT session_id) FROM errors;", fetch_one=True))[0]
        summary["error_rate_sessions"] = (sessions_with_errors / summary["total_sessions"] * 100) if summary["total_sessions"] > 0 else 0.0

        summary["avg_feedback_score"] = (await self._execute("SELECT AVG(score) FROM feedback WHERE type = 'rating';", fetch_one=True))[0] or "N/A"

        top_error_types_rows = await self._execute("SELECT error_type, COUNT(*) as count FROM errors GROUP BY error_type ORDER BY count DESC LIMIT 3;", fetch_all=True)
        summary["top_error_types"] = [dict(row) for row in top_error_types_rows]

        top_models_rows = await self._execute("SELECT model_name, SUM(tokens_in + tokens_out) as total_tokens FROM messages WHERE model_name IS NOT NULL GROUP BY model_name ORDER BY total_tokens DESC LIMIT 3;", fetch_all=True)
        summary["top_models_by_tokens"] = [dict(row) for row in top_models_rows]

        return summary

    async def get_metrics_time_series(self, metric_name: str, interval: str,
                                      start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves time-series data for a specific metric, aggregated by a given interval.

        :param metric_name: The name of the metric.
        :type metric_name: str
        :param interval: The time aggregation interval ('hour', 'day').
        :type interval: str
        :param start_date: Filter data starting after this date (YYYY-MM-DD). Defaults to None.
        :type start_date: Optional[str]
        :param end_date: Filter data ending before this date (YYYY-MM-DD). Defaults to None.
        :type end_date: Optional[str]
        :returns: A list of dictionaries with time buckets and aggregated values.
        :rtype: List[Dict[str, Any]]
        """
        if interval == 'hour':
            pg_time_trunc = 'hour'
            pg_time_format = 'YYYY-MM-DD HH24:MI:SS'
        else:
            pg_time_trunc = 'day'
            pg_time_format = 'YYYY-MM-DD HH24:MI:SS'

        query = f"""
            SELECT 
                TO_CHAR(DATE_TRUNC('{pg_time_trunc}', timestamp), '{pg_time_format}') as time_bucket,
                SUM(value) as total_value
            FROM metrics
            WHERE name = $1
        """
        params = [metric_name]
        param_counter = 2

        if start_date:
            query += f" AND timestamp >= ${param_counter}"
            params.append(start_date + " 00:00:00")
            param_counter += 1
        if end_date:
            query += f" AND timestamp <= ${param_counter}"
            params.append(end_date + " 23:59:59")
            param_counter += 1

        query += " GROUP BY time_bucket ORDER BY time_bucket ASC;"
        
        rows = await self._execute(query, tuple(params), fetch_all=True)
        return [dict(row) for row in rows]

    async def get_model_token_usage(self) -> List[Dict[str, Any]]:
        """
        Retrieves aggregated token usage per model across all messages.

        :returns: A list of dictionaries with 'model_name' and 'total_tokens' for each model,
                  ordered by total tokens in descending order.
        :rtype: List[Dict[str, Any]]
        """
        query = """
            SELECT model_name, SUM(tokens_in + tokens_out) as total_tokens
            FROM messages
            WHERE model_name IS NOT NULL
            GROUP BY model_name
            ORDER BY total_tokens DESC;
        """
        rows = await self._execute(query, fetch_all=True)
        return [dict(row) for row in rows]

    async def get_feedback_score_distribution(self) -> List[Dict[str, Any]]:
        """
        Retrieves the distribution of feedback scores for 'rating' type feedback.

        :returns: A list of dictionaries, each with a 'score' and its 'count',
                  ordered by score in ascending order.
        :rtype: List[Dict[str, Any]]
        """
        query = """
            SELECT score, COUNT(id) as count
            FROM feedback
            WHERE type = 'rating' AND score IS NOT NULL
            GROUP BY score
            ORDER BY score ASC;
        """
        rows = await self._execute(query, fetch_all=True)
        return [dict(row) for row in rows]

    async def get_error_type_counts(self) -> List[Dict[str, Any]]:
        """
        Retrieves the counts of different error types recorded.

        :returns: A list of dictionaries, each with an 'error_type' and its 'count',
                  ordered by count in descending order.
        :rtype: List[Dict[str, Any]]
        """
        query = """
            SELECT error_type, COUNT(id) as count
            FROM errors
            WHERE error_type IS NOT NULL
            GROUP BY error_type
            ORDER BY count DESC;
        """
        rows = await self._execute(query, fetch_all=True)
        return [dict(row) for row in rows]

    async def get_avg_session_duration(self) -> float:
        """
        Retrieves the average duration of completed sessions in seconds.

        Calculates the average difference between `end_time` and `start_time` for sessions
        where `end_time` is not null.

        :returns: The average session duration in seconds. Returns 0.0 if no completed sessions.
        :rtype: float
        """
        query = """
            SELECT AVG(EXTRACT(EPOCH FROM (end_time - start_time))) AS avg_duration_seconds
            FROM sessions
            WHERE end_time IS NOT NULL;
        """
        result = await self._execute(query, fetch_one=True)
        return result[0] if result and result[0] is not None else 0.0
