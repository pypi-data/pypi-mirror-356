import pytest
import os
from datetime import datetime, timedelta
from llmtrace.storage.sqlite import SQLiteBackend # Import SQLiteBackend directly for testing
import aiosqlite # Use aiosqlite for async DB operations

# Use a temporary database for testing
@pytest.fixture(scope="function")
async def temp_db_path(tmp_path): # Made async
    db_file = tmp_path / "test_llmtrace.db"
    return str(db_file)

@pytest.fixture(scope="function")
async def db_instance(temp_db_path): # Made async
    # Ensure a fresh instance for each test
    SQLiteBackend._instance = None 
    db = SQLiteBackend(temp_db_path)
    await db.connect() # Await connection
    yield db
    await db.close() # Await close
    # Clean up the database file after the test
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)

@pytest.mark.asyncio # Mark test as async
async def test_database_initialization(db_instance, temp_db_path): # Made async
    assert os.path.exists(temp_db_path)
    conn = await aiosqlite.connect(temp_db_path) # Use aiosqlite.connect
    cursor = await conn.cursor()
    await cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in await cursor.fetchall()]
    assert "sessions" in tables
    assert "messages" in tables
    assert "metrics" in tables
    assert "feedback" in tables
    assert "errors" in tables
    await conn.close()

@pytest.mark.asyncio # Mark test as async
async def test_insert_and_get_session(db_instance): # Made async
    start_time = datetime.now()
    session = db_instance.Session(start_time=start_time) # Use db_instance.Session
    session_id = await db_instance.insert_session(session) # Await DB operation
    assert session_id is not None
    assert session.id == session_id

    retrieved_session = await db_instance.get_session(session_id) # Await DB operation
    assert retrieved_session is not None
    assert retrieved_session.id == session_id
    assert retrieved_session.start_time.isoformat() == start_time.isoformat()
    assert retrieved_session.total_tokens == 0
    assert retrieved_session.total_cost == 0.0

@pytest.mark.asyncio # Mark test as async
async def test_update_session(db_instance): # Made async
    session = db_instance.Session(start_time=datetime.now()) # Use db_instance.Session
    session_id = await db_instance.insert_session(session) # Await DB operation

    updated_session = await db_instance.get_session(session_id) # Await DB operation
    updated_session.end_time = datetime.now() + timedelta(minutes=5)
    updated_session.total_tokens = 100
    updated_session.total_cost = 0.05
    await db_instance.update_session(updated_session) # Await DB operation

    retrieved_session = await db_instance.get_session(session_id) # Await DB operation
    assert retrieved_session.end_time.isoformat() == updated_session.end_time.isoformat()
    assert retrieved_session.total_tokens == 100
    assert retrieved_session.total_cost == 0.05

@pytest.mark.asyncio # Mark test as async
async def test_insert_and_get_message(db_instance): # Made async
    session = db_instance.Session(start_time=datetime.now()) # Use db_instance.Session
    session_id = await db_instance.insert_session(session) # Await DB operation

    message = db_instance.Message( # Use db_instance.Message
        session_id=session_id,
        role="user",
        content="Hello LLM!",
        timestamp=datetime.now(),
        tokens_in=10,
        tokens_out=0,
        cost=0.0
    )
    message_id = await db_instance.insert_message(message) # Await DB operation
    assert message_id is not None
    assert message.id == message_id

    messages = await db_instance.get_messages_for_session(session_id) # Await DB operation
    assert len(messages) == 1
    assert messages[0].content == "Hello LLM!"

@pytest.mark.asyncio # Mark test as async
async def test_insert_metric(db_instance): # Made async
    session = db_instance.Session(start_time=datetime.now()) # Use db_instance.Session
    session_id = await db_instance.insert_session(session) # Await DB operation

    metric = db_instance.Metric( # Use db_instance.Metric
        session_id=session_id,
        name="latency",
        value=0.5,
        timestamp=datetime.now()
    )
    await db_instance.insert_metric(metric) # Await DB operation

    metrics = await db_instance.get_metrics_for_session(session_id) # Await DB operation
    assert len(metrics) == 1
    assert metrics[0].name == "latency"
    assert metrics[0].value == 0.5

@pytest.mark.asyncio # Mark test as async
async def test_insert_feedback(db_instance): # Made async
    session = db_instance.Session(start_time=datetime.now()) # Use db_instance.Session
    session_id = await db_instance.insert_session(session) # Await DB operation
    message = db_instance.Message(session_id=session_id, role="user", content="test", timestamp=datetime.now()) # Use db_instance.Message
    message_id = await db_instance.insert_message(message) # Await DB operation

    feedback = db_instance.Feedback( # Use db_instance.Feedback
        session_id=session_id,
        message_id=message_id,
        type="rating", # Added type
        score=5, # Changed from rating to score
        comment="Excellent!",
        timestamp=datetime.now()
    )
    await db_instance.insert_feedback(feedback) # Await DB operation

    feedbacks = await db_instance.get_feedback_for_session(session_id) # Await DB operation
    assert len(feedbacks) == 1
    assert feedbacks[0].score == 5 # Changed from rating to score
    assert feedbacks[0].comment == "Excellent!"

@pytest.mark.asyncio # Mark test as async
async def test_insert_error(db_instance): # Made async
    session = db_instance.Session(start_time=datetime.now()) # Use db_instance.Session
    session_id = await db_instance.insert_session(session) # Await DB operation

    error = db_instance.Error( # Use db_instance.Error
        session_id=session_id,
        message="API call failed",
        details="Network error",
        timestamp=datetime.now()
    )
    await db_instance.insert_error(error) # Await DB operation

    errors = await db_instance.get_errors_for_session(session_id) # Await DB operation
    assert len(errors) == 1
    assert errors[0].message == "API call failed"
    assert errors[0].details == "Network error"

@pytest.mark.asyncio # Mark test as async
async def test_get_all_sessions(db_instance): # Made async
    session1 = db_instance.Session(start_time=datetime.now() - timedelta(hours=1)) # Use db_instance.Session
    session2 = db_instance.Session(start_time=datetime.now()) # Use db_instance.Session
    await db_instance.insert_session(session1) # Await DB operation
    await db_instance.insert_session(session2) # Await DB operation

    all_sessions = await db_instance.get_all_sessions() # Await DB operation
    assert len(all_sessions) == 2
    # Should be ordered by start_time DESC
    assert all_sessions[0].id == session2.id
    assert all_sessions[1].id == session1.id
