"""
SQLite backend implementation for LLMTrace.

This module provides a concrete implementation of the :class:`llmtrace.storage.backends.StorageBackend`
abstract interface using `aiosqlite` for asynchronous SQLite database operations.
It handles database connection, table creation, and CRUD operations for sessions,
messages, metrics, feedback, and errors, including content compression.
"""

import aiosqlite
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
import zlib

from llmtrace.tracing.models import Session, Message, Metric, Feedback, Error
from llmtrace.storage.backends import StorageBackend

class SQLiteBackend(StorageBackend):
    """
    Singleton class for managing the SQLite database connection and operations.

    Implements the :class:`llmtrace.storage.backends.StorageBackend` abstract interface.
    Ensures only one instance of the database connection exists throughout the application.
    """
    _instance = None

    def __new__(cls, db_path: str = '~/.llmtrace/llmtrace.db'):
        """
        Ensures only one instance of the SQLiteBackend class exists (Singleton pattern).

        :param db_path: Path to the SQLite database file. Defaults to '~/.llmtrace/llmtrace.db'.
        :type db_path: str
        :returns: The singleton instance of SQLiteBackend.
        :rtype: SQLiteBackend
        """
        if cls._instance is None:
            cls._instance = super(SQLiteBackend, cls).__new__(cls)
            cls._instance._initialized = False
            cls._instance.db_path = os.path.expanduser(db_path)
        return cls._instance

    def __init__(self, db_path: str = '~/.llmtrace/llmtrace.db'):
        """
        Initializes the SQLiteBackend instance.

        Ensures the database directory exists and sets up the path.
        The actual connection and table creation are handled by asynchronous methods.

        :param db_path: Path to the SQLite database file. Defaults to '~/.llmtrace/llmtrace.db'.
        :type db_path: str
        """
        if self._initialized:
            return
        self.db_path = os.path.expanduser(db_path)
        self._connection: Optional[aiosqlite.Connection] = None
        self._initialized = True
        self._ensure_db_directory()

    def _ensure_db_directory(self) -> None:
        """
        Ensures the directory for the SQLite database file exists.
        Creates the directory if it does not already exist.
        """
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    async def connect(self) -> None:
        """
        Establishes an asynchronous SQLite database connection.

        Sets `row_factory` to `aiosqlite.Row` for convenient column access by name.
        Also calls `create_tables()` to ensure the schema is present.
        """
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.db_path)
            self._connection.row_factory = aiosqlite.Row
            await self.create_tables()

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
        :returns: Fetched row(s) (aiosqlite.Row or list of aiosqlite.Row) or the cursor object for non-fetch operations.
        :rtype: Any
        """
        conn = await self._get_connection()
        async with conn.cursor() as cursor:
            await cursor.execute(query, params)
            if fetch_one:
                return await cursor.fetchone()
            if fetch_all:
                return await cursor.fetchall()
            await conn.commit()
            return cursor

    async def _get_connection(self) -> aiosqlite.Connection:
        """
        Internal method to get the current active database connection, ensuring it's open.

        If the connection is not yet established, it calls `connect()` to open it.

        :returns: The active aiosqlite database connection.
        :rtype: aiosqlite.Connection
        """
        if self._connection is None:
            await self.connect()
        return self._connection

    async def create_tables(self) -> None:
        """
        Creates the necessary tables in the database if they do not already exist.

        Also includes ALTER TABLE statements to add new columns that might have been
        introduced in later versions, ensuring backward compatibility for existing databases.
        """
        queries = [
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                total_tokens INTEGER DEFAULT 0,
                total_cost REAL DEFAULT 0.0,
                user_id TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content BLOB NOT NULL,
                timestamp TEXT NOT NULL,
                tokens_in INTEGER DEFAULT 0,
                tokens_out INTEGER DEFAULT 0,
                cost REAL DEFAULT 0.0,
                model_name TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                message_id INTEGER,
                type TEXT NOT NULL,
                score INTEGER,
                comment TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                message_id INTEGER,
                error_type TEXT,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                details TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
            );
            """
        ]
        for query in queries:
            await self._execute(query)
        
        # Add ALTER TABLE statements for existing databases if columns are missing
        await self._add_column_if_not_exists("sessions", "name", "TEXT")
        await self._add_column_if_not_exists("sessions", "user_id", "TEXT")
        await self._add_column_if_not_exists("messages", "model_name", "TEXT")
        await self._add_column_if_not_exists("feedback", "type", "TEXT DEFAULT 'rating'")
        await self._add_column_if_not_exists("feedback", "score", "INTEGER")
        await self._add_column_if_not_exists("errors", "message_id", "INTEGER")
        await self._add_column_if_not_exists("errors", "error_type", "TEXT")

    async def _add_column_if_not_exists(self, table_name: str, column_name: str, column_type: str) -> None:
        """
        Adds a column to a table if it does not already exist.

        This is a helper for `create_tables` to handle schema evolution without full migrations.
        For production, a dedicated migration tool like Alembic is recommended.

        :param table_name: The name of the table.
        :type table_name: str
        :param column_name: The name of the column to add.
        :type column_name: str
        :param column_type: The SQL type of the column (e.g., 'TEXT', 'INTEGER').
        :type column_type: str
        """
        conn = await self._get_connection()
        async with conn.cursor() as cursor:
            try:
                await cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [col[1] for col in await cursor.fetchall()]
                if column_name not in columns:
                    await cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")
                    await conn.commit()
                    print(f"Added column '{column_name}' to table '{table_name}'.")
            except aiosqlite.OperationalError as e:
                print(f"Could not add column {column_name} to {table_name}: {e}")

    async def insert_session(self, session: Session) -> int:
        """
        Inserts a new session into the database.

        :param session: The Session object to insert.
        :type session: Session
        :returns: The ID of the newly inserted session.
        :rtype: int
        """
        cursor = await self._execute(
            "INSERT INTO sessions (name, start_time, user_id) VALUES (?, ?, ?)",
            (session.name, session.start_time.isoformat(), session.user_id)
        )
        session.id = cursor.lastrowid
        return session.id

    async def update_session(self, session: Session) -> None:
        """
        Updates an existing session in the database.

        :param session: The Session object with updated values.
        :type session: Session
        """
        await self._execute(
            "UPDATE sessions SET name = ?, end_time = ?, total_tokens = ?, total_cost = ?, user_id = ? WHERE id = ?",
            (session.name,
             session.end_time.isoformat() if session.end_time else None,
             session.total_tokens,
             session.total_cost,
             session.user_id,
             session.id)
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
        cursor = await self._execute(
            "INSERT INTO messages (session_id, role, content, timestamp, tokens_in, tokens_out, cost, model_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (message.session_id, message.role, compressed_content, message.timestamp.isoformat(),
             message.tokens_in, message.tokens_out, message.cost, message.model_name)
        )
        message.id = cursor.lastrowid
        return message.id

    async def insert_metric(self, metric: Metric) -> None:
        """
        Inserts a new metric into the database.

        :param metric: The Metric object to insert.
        :type metric: Metric
        """
        await self._execute(
            "INSERT INTO metrics (session_id, name, value, timestamp) VALUES (?, ?, ?, ?)",
            (metric.session_id, metric.name, metric.value, metric.timestamp.isoformat())
        )

    async def insert_feedback(self, feedback: Feedback) -> None:
        """
        Inserts new feedback into the database.

        :param feedback: The Feedback object to insert.
        :type feedback: Feedback
        """
        await self._execute(
            "INSERT INTO feedback (session_id, message_id, type, score, comment, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (feedback.session_id, feedback.message_id, feedback.type, feedback.score, feedback.comment, feedback.timestamp.isoformat())
        )

    async def insert_error(self, error: Error) -> None:
        """
        Inserts a new error into the database.

        :param error: The Error object to insert.
        :type error: Error
        """
        await self._execute(
            "INSERT INTO errors (session_id, message_id, error_type, message, timestamp, details) VALUES (?, ?, ?, ?, ?, ?)",
            (error.session_id, error.message_id, error.error_type, error.message, error.timestamp.isoformat(), error.details)
        )

    async def close(self) -> None:
        """
        Closes the database connection.
        """
        if self._connection:
            await self._connection.close()
            self._connection = None

    async def get_session(self, session_id: int) -> Optional[Session]:
        """
        Retrieves a single session by its ID.

        :param session_id: The ID of the session to retrieve.
        :type session_id: int
        :returns: The Session object if found, otherwise None.
        :rtype: Optional[Session]
        """
        row = await self._execute("SELECT * FROM sessions WHERE id = ?", (session_id,), fetch_one=True)
        return Session.from_db_row(row) if row else None

    async def get_messages_for_session(self, session_id: int) -> List[Message]:
        """
        Retrieves all messages for a given session ID. Message content is decompressed.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Message objects.
        :rtype: List[Message]
        """
        rows = await self._execute("SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp ASC", (session_id,), fetch_all=True)
        return [Message.from_db_row(row) for row in rows]

    async def get_all_sessions(self) -> List[Session]:
        """
        Retrieves all sessions from the database, ordered by start time descending.

        :returns: A list of Session objects.
        :rtype: List[Session]
        """
        rows = await self._execute("SELECT * FROM sessions ORDER BY start_time DESC", fetch_all=True)
        return [Session.from_db_row(row) for row in rows]

    async def get_metrics_for_session(self, session_id: int) -> List[Metric]:
        """
        Retrieves all metrics for a given session ID.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Metric objects.
        :rtype: List[Metric]
        """
        rows = await self._execute("SELECT * FROM metrics WHERE session_id = ? ORDER BY timestamp ASC", (session_id,), fetch_all=True)
        return [Metric.from_db_row(row) for row in rows]

    async def get_feedback_for_session(self, session_id: int) -> List[Feedback]:
        """
        Retrieves all feedback entries for a given session ID.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Feedback objects.
        :rtype: List[Feedback]
        """
        rows = await self._execute("SELECT * FROM feedback WHERE session_id = ? ORDER BY timestamp ASC", (session_id,), fetch_all=True)
        return [Feedback.from_db_row(row) for row in rows]

    async def get_errors_for_session(self, session_id: int) -> List[Error]:
        """
        Retrieves all error entries for a given session ID.

        :param session_id: The ID of the session.
        :type session_id: int
        :returns: A list of Error objects.
        :rtype: List[Error]
        """
        rows = await self._execute("SELECT * FROM errors WHERE session_id = ? ORDER BY timestamp ASC", (session_id,), fetch_all=True)
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
                                      Note: This is a simplified approach for compressed content.
                                      A more robust solution might involve full-text search.
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

        if message_content_search or model_name:
            joins.append("JOIN messages m ON s.id = m.session_id")

        if start_time:
            where_clauses.append("s.start_time >= ?")
            params.append(start_time)
        if end_time:
            where_clauses.append("s.end_time <= ?")
            params.append(end_time)
        if session_name:
            where_clauses.append("s.name LIKE ?")
            params.append(f"%{session_name}%")
        if user_id:
            where_clauses.append("s.user_id LIKE ?")
            params.append(f"%{user_id}%")
        if message_content_search:
            compressed_search_term = zlib.compress(message_content_search.encode('utf-8'))
            where_clauses.append("HEX(m.content) LIKE ?")
            params.append(f"%{compressed_search_term.hex()}%")
        if model_name:
            where_clauses.append("m.model_name LIKE ?")
            params.append(f"%{model_name}%")
        if min_tokens is not None:
            where_clauses.append("s.total_tokens >= ?")
            params.append(min_tokens)
        if max_tokens is not None:
            where_clauses.append("s.total_tokens <= ?")
            params.append(max_tokens)
        if min_cost is not None:
            where_clauses.append("s.total_cost >= ?")
            params.append(min_cost)
        if max_cost is not None:
            where_clauses.append("s.total_cost <= ?")
            params.append(max_cost)

        if joins:
            query += " " + " ".join(joins)
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += " ORDER BY s.start_time DESC"
        
        rows = await self._execute(query, tuple(params), fetch_all=True)
        return [Session.from_db_row(row) for row in rows]

    async def delete_session(self, session_id: int) -> None:
        """
        Deletes a session and all its associated data (messages, metrics, feedback, errors).
        This operation relies on `ON DELETE CASCADE` foreign key constraints defined during table creation.

        :param session_id: The ID of the session to delete.
        :type session_id: int
        """
        await self._execute("DELETE FROM sessions WHERE id = ?", (session_id,))
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

        summary["total_sessions"] = (await self._execute("SELECT COUNT(id) FROM sessions", fetch_one=True))[0]
        summary["total_messages"] = (await self._execute("SELECT COUNT(id) FROM messages", fetch_one=True))[0]
        summary["total_tokens_overall"] = (await self._execute("SELECT SUM(total_tokens) FROM sessions", fetch_one=True))[0] or 0
        summary["total_cost_overall"] = (await self._execute("SELECT SUM(total_cost) FROM sessions", fetch_one=True))[0] or 0.0
        summary["avg_tokens_per_session"] = (await self._execute("SELECT AVG(total_tokens) FROM sessions", fetch_one=True))[0] or 0.0
        summary["avg_cost_per_session"] = (await self._execute("SELECT AVG(total_cost) FROM sessions", fetch_one=True))[0] or 0.0

        sessions_with_errors = (await self._execute("SELECT COUNT(DISTINCT session_id) FROM errors", fetch_one=True))[0]
        summary["error_rate_sessions"] = (sessions_with_errors / summary["total_sessions"] * 100) if summary["total_sessions"] > 0 else 0.0

        summary["avg_feedback_score"] = (await self._execute("SELECT AVG(score) FROM feedback WHERE type = 'rating'", fetch_one=True))[0] or "N/A"

        top_error_types_rows = await self._execute("SELECT error_type, COUNT(*) as count FROM errors GROUP BY error_type ORDER BY count DESC LIMIT 3", fetch_all=True)
        summary["top_error_types"] = [dict(row) for row in top_error_types_rows]

        top_models_rows = await self._execute("SELECT model_name, SUM(tokens_in + tokens_out) as total_tokens FROM messages WHERE model_name IS NOT NULL GROUP BY model_name ORDER BY total_tokens DESC LIMIT 3", fetch_all=True)
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
            time_format = '%Y-%m-%d %H:00:00'
        else: # default to day
            time_format = '%Y-%m-%d 00:00:00'

        query = f"""
            SELECT 
                strftime('{time_format}', timestamp) as time_bucket,
                SUM(value) as total_value
            FROM metrics
            WHERE name = ?
        """
        params = [metric_name]
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date + " 00:00:00")
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date + " 23:59:59")

        query += " GROUP BY time_bucket ORDER BY time_bucket ASC"
        
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
            SELECT AVG(JULIANDAY(end_time) - JULIANDAY(start_time)) * 24 * 60 * 60 AS avg_duration_seconds
            FROM sessions
            WHERE end_time IS NOT NULL;
        """
        result = await self._execute(query, fetch_one=True)
        return result[0] if result and result[0] is not None else 0.0
