import pytest
import os
import asyncio # Import asyncio
from datetime import datetime
from llmtrace.core import core
from llmtrace.storage.sqlite import SQLiteBackend # Import SQLiteBackend directly for testing
from llmtrace.tracing.models import Session, Message, Metric, Feedback, Error

# Use a temporary database for testing
@pytest.fixture(scope="function")
async def temp_db_path(tmp_path): # Made async
    db_file = tmp_path / "test_llmtrace_core.db"
    return str(db_file)

@pytest.fixture(scope="function")
async def setup_llmtrace(temp_db_path): # Made async
    # Reset singleton and initialize for each test
    core._db_instance = None
    core._current_session_id = None
    await core.init(temp_db_path) # Await core.init
    yield
    # Clean up after test
    if core._db_instance:
        await core._db_instance.close() # Await close
        core._db_instance = None
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)

@pytest.mark.asyncio # Mark test as async
async def test_init(setup_llmtrace, temp_db_path): # Made async
    assert core._db_instance is not None
    assert isinstance(core._db_instance, SQLiteBackend) # Check against SQLiteBackend
    assert core._db_instance.db_path == temp_db_path

@pytest.mark.asyncio # Mark test as async
async def test_create_and_end_session(setup_llmtrace): # Made async
    session_id = await core.session(name="TestSession", user_id="test_user").__aenter__() # Await async context manager entry
    assert session_id is not None
    assert core.get_current_session_id() == session_id

    session = await core._db_instance.get_session(session_id) # Await DB operation
    assert session is not None
    assert session.id == session_id
    assert session.end_time is None

    # Simulate ending the session by calling __aexit__
    await core.session(name="TestSession", user_id="test_user").__aexit__(None, None, None) # Await async context manager exit
    assert core.get_current_session_id() is None

    ended_session = await core._db_instance.get_session(session_id) # Await DB operation
    assert ended_session.end_time is not None
    # The total_tokens and total_cost will be 0 because no messages were logged
    assert ended_session.total_tokens == 0
    assert ended_session.total_cost == 0.0

@pytest.mark.asyncio # Mark test as async
async def test_log_message(setup_llmtrace): # Made async
    session_id = await core.session().__aenter__() # Await async context manager entry
    message_id = await core.log_message(session_id, "user", "Test prompt", tokens_in=5, tokens_out=0, cost=0.0) # Await log_message
    assert message_id is not None

    messages = await core._db_instance.get_messages_for_session(session_id) # Await DB operation
    assert len(messages) == 1
    assert messages[0].content == "Test prompt"
    assert messages[0].role == "user"
    assert messages[0].tokens_in == 5
    await core.session().__aexit__(None, None, None) # Await async context manager exit

@pytest.mark.asyncio # Mark test as async
async def test_log_metric(setup_llmtrace): # Made async
    session_id = await core.session().__aenter__() # Await async context manager entry
    await core.log_metric(session_id, "latency_ms", 123.45) # Await log_metric

    metrics = await core._db_instance.get_metrics_for_session(session_id) # Await DB operation
    assert len(metrics) == 1
    assert metrics[0].name == "latency_ms"
    assert metrics[0].value == 123.45
    await core.session().__aexit__(None, None, None) # Await async context manager exit

@pytest.mark.asyncio # Mark test as async
async def test_log_feedback(setup_llmtrace): # Made async
    session_id = await core.session().__aenter__() # Await async context manager entry
    message_id = await core.log_message(session_id, "assistant", "Response", tokens_in=0, tokens_out=10, cost=0.01) # Await log_message
    await core.add_feedback(session_id, 4, message_id, "Good response, but could be better.") # Await add_feedback

    feedback = await core._db_instance.get_feedback_for_session(session_id) # Await DB operation
    assert len(feedback) == 1
    assert feedback[0].score == 4 # Changed from rating to score
    assert feedback[0].comment == "Good response, but could be better."
    assert feedback[0].message_id == message_id
    await core.session().__aexit__(None, None, None) # Await async context manager exit

@pytest.mark.asyncio # Mark test as async
async def test_log_error(setup_llmtrace): # Made async
    session_id = await core.session().__aenter__() # Await async context manager entry
    await core.log_error(session_id, "Failed to connect", "Connection refused by server.") # Await log_error

    errors = await core._db_instance.get_errors_for_session(session_id) # Await DB operation
    assert len(errors) == 1
    assert errors[0].message == "Failed to connect"
    assert errors[0].details == "Connection refused by server."
    await core.session().__aexit__(None, None, None) # Await async context manager exit

@pytest.mark.asyncio # Mark test as async
async def test_no_session_warning(capsys, setup_llmtrace): # Made async
    # Ensure no session is active
    core._current_session_id = None 
    await core.log_message(123, "user", "Should not log") # Await log_message
    captured = capsys.readouterr()
    assert "Warning: LLMTrace not initialized. Message not logged." in captured.out

    # Re-initialize to test warning when DB is not initialized
    if core._db_instance:
        await core._db_instance.close() # Await close
    core._db_instance = None
    await core.log_message(123, "user", "Should not log") # Await log_message
    captured = capsys.readouterr()
    assert "Warning: LLMTrace not initialized. Message not logged." in captured.out
