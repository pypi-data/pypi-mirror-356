Usage
=====

This section provides examples on how to use LLMTrace in your applications.

Initialization
--------------

Always initialize LLMTrace at the start of your application:

.. code-block:: python

   import llmtrace

   # The database will be created in ~/.llmtrace/llmtrace.db by default
   # You can specify a different path and an application name
   llmtrace.init(db_path="./my_app_trace.db", app_name="MyChatApplication")

Instrumentation
---------------

LLMTrace provides automatic instrumentation for popular LLM frameworks.

.. toctree::
   :maxdepth: 1

   usage/openai_instrumentation
   usage/huggingface_instrumentation
   usage/langchain_instrumentation

Session Management
------------------

You can group interactions into logical sessions using the asynchronous context manager:

.. code-block:: python

   import llmtrace
   import openai
   import asyncio

   async def main():
       llmtrace.init()
       llmtrace.OpenAIInstrumentor().instrument()

       async with llmtrace.session(name="TestSession", user_id="user_123") as session_id:
           print(f"Active session ID: {session_id}")
           await openai.ChatCompletion.create(
               model="gpt-3.5-turbo",
               messages=[{"role": "user", "content": "Hello, how are you?"}]
           )
           # All LLM calls within this block are associated with this session

   if __name__ == "__main__":
       asyncio.run(main())

User Feedback
-------------

Record explicit feedback from your users:

.. code-block:: python

   import llmtrace
   import asyncio

   async def main():
       llmtrace.init()

       # Assuming you have a session_id and message_id from a previous interaction
       example_session_id = 1
       example_message_id = 5

       await llmtrace.add_feedback(
           session_id=example_session_id,
           message_id=example_message_id,
           score=5, # Use 'score'
           comment="Excellent and very helpful response!",
           feedback_type="rating" # Or "thumb_up", "thumb_down"
       )

   if __name__ == "__main__":
       asyncio.run(main())

Programmatic Queries
--------------------

Access traceability data directly from your Python code asynchronously:

.. code-block:: python

   import llmtrace
   import asyncio

   async def main():
       llmtrace.init()

       all_sessions = await llmtrace.get_sessions()
       print(f"Total sessions: {len(all_sessions)}")

       if all_sessions:
           first_session_id = all_sessions[0].id
           messages = await llmtrace.get_messages(first_session_id)
           print(f"Messages in the first session ({first_session_id}):")
           for msg in messages:
               print(f"- {msg.role}: {msg.content[:50]}...")

           metrics = await llmtrace.get_metrics(first_session_id)
           print(f"Metrics in the first session ({first_session_id}):")
           for metric in metrics:
               print(f"- {metric.name}: {metric.value}")

   if __name__ == "__main__":
       asyncio.run(main())

CLI Usage
---------

LLMTrace installs an `llmtrace` command in your terminal:

*   **List sessions:**
    .. code-block:: bash

       llmtrace sessions

*   **Show session details:**
    .. code-block:: bash

       llmtrace show <session_id>
       # Example: llmtrace show 1

*   **Export data:**
    .. code-block:: bash

       llmtrace export --format json --output my_data.json
       llmtrace export --id <session_id> --format csv
       # Example: llmtrace export --id 1 --format json

*   **Delete a session:**
    .. code-block:: bash

       llmtrace delete <session_id>
       # Ejemplo: llmtrace delete 1

*   **Show aggregated metrics:**
    .. code-block:: bash

       llmtrace metrics

*   **Start the web dashboard:**
    .. code-block:: bash

       llmtrace web --port 8000 --no-browser

Dashboard Deployment with Docker
--------------------------------

You can deploy the LLMTrace web dashboard using Docker. Ensure Docker is installed.

1.  **Build the Docker image:**
    .. code-block:: bash

       docker build -t llmtrace-dashboard .

2.  **Run the container:**
    .. code-block:: bash

    docker run -p 5000:5000 llmtrace-dashboard

The dashboard will be available at `http://localhost:5000`.
