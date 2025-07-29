"""
Storage backend factory for LLMTrace.

Provides a function to get the appropriate storage backend based on configuration,
allowing LLMTrace to seamlessly switch between different database systems.
"""

import os
from typing import Optional
from llmtrace.storage.backends import StorageBackend
from llmtrace.storage.sqlite import SQLiteBackend
from llmtrace.storage.postgresql import PostgreSQLBackend

async def get_storage_backend(backend_type: Optional[str] = None, **kwargs) -> StorageBackend:
    """
    Returns an instance of the configured storage backend.

    The backend type can be specified explicitly or via the `LLMTRACE_STORAGE_BACKEND`
    environment variable. Defaults to 'sqlite'.

    :param backend_type: The type of backend to use ('sqlite', 'postgresql').
                         Defaults to 'sqlite' if not specified or via env var.
    :type backend_type: Optional[str]
    :param kwargs: Additional keyword arguments to pass to the backend constructor.
                   For 'sqlite', `db_path` can be provided.
                   For 'postgresql', `connection_string` can be provided.
    :type kwargs: Any
    :returns: An instance of the selected storage backend.
    :rtype: StorageBackend
    :raises ValueError: If an unsupported backend type is specified.
    """
    backend_type = backend_type or os.getenv("LLMTRACE_STORAGE_BACKEND", "sqlite").lower()

    if backend_type == "sqlite":
        db_path = kwargs.get("db_path", '~/.llmtrace/llmtrace.db')
        backend = SQLiteBackend(db_path=db_path)
    elif backend_type == "postgresql":
        connection_string = kwargs.get("connection_string")
        backend = PostgreSQLBackend(connection_string=connection_string)
    else:
        raise ValueError(f"Unsupported storage backend type: {backend_type}. Supported types are 'sqlite', 'postgresql'.")
    
    await backend.connect()
    return backend
