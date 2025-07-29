import time
import os
import asyncio # Import asyncio
import llmtrace # Import the top-level package
from llmtrace.instrumentation.openai import mock_openai # Still need mock for demo
from llmtrace.instrumentation.huggingface import MockPipeline # Still need mock for demo
from llmtrace.tracing.models import Session, Message, Metric, Feedback, Error # Import models for verification
from llmtrace.evaluation.evaluation import evaluate_response_length, evaluate_basic_toxicity, evaluate_llm_as_judge, TestCase, run_static_test_set, evaluate_sentiment, evaluate_topic_relevancy
from llmtrace.dashboard.app import create_dashboard_app # Import dashboard app factory

# --- Mock LangChain for demonstration purposes ---
class MockChatOpenAI:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.model_name = model_name

    async def invoke(self, input_text, config=None): # Made invoke async
        print(f"Mock LangChain: Invoking {self.model_name} with: {input_text}")
        response_content = f"LangChain mock response to: '{input_text[:50]}...'"
        
        prompt_tokens = len(input_text.split()) * 1.2
        completion_tokens = len(response_content.split()) * 1.2
        total_tokens = prompt_tokens + completion_tokens

        class MockLLMResult:
            def __init__(self, generations, llm_output):
                self.generations = generations
                self.llm_output = llm_output
        
        return_value = MockLLMResult(
            generations=[[type('Generation', (object,), {'text': response_content})()]],
            llm_output={
                "token_usage": {
                    "prompt_tokens": int(prompt_tokens),
                    "completion_tokens": int(completion_tokens),
                    "total_tokens": int(total_tokens),
                },
                "model_name": self.model_name,
            }
        )
        return return_value

# --------------------------------------------------

async def run_llm_interactions_and_evaluations(): # Made main function async
    # 1. Initialize LLMTrace with app name
    await llmtrace.init(app_name="MyDemoApp") # Await init

    # 2. Instrument LLMs (this would typically be done once at app startup)
    openai_instrumentor = llmtrace.OpenAIInstrumentor()
    openai_instrumentor.instrument()

    hf_instrumentor = llmtrace.HFInstrumentor()
    # Apply HuggingFace instrumentation to our mock pipeline
    @hf_instrumentor.instrument_pipeline
    class InstrumentedMockPipeline(MockPipeline):
        pass

    # 3. Use the session context manager
    async with llmtrace.session(name="MyFirstChatSession", user_id="user_123") as session_id: # Use async with
        print(f"\n--- Active Session ID: {session_id} ---")

        print("\n--- Simulating OpenAI Interaction ---")
        try:
            openai_response = mock_openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": "Tell me a short story about a brave knight who saved a dragon."}]
            )
            openai_content = openai_response['choices'][0]['message']['content']
            print(f"OpenAI Response: {openai_content[:100]}...")
            
            # Evaluate OpenAI response
            length = evaluate_response_length(openai_content)
            toxicity = evaluate_basic_toxicity(openai_content)
            await llmtrace.log_metric(session_id, "openai_response_length", float(length)) # Await log_metric
            await llmtrace.log_metric(session_id, "openai_response_toxicity", toxicity) # Await log_metric
            print(f"  Evaluated Length: {length}, Basic Toxicity: {toxicity:.2f}")

            # Simulate LLM-as-judge (assuming message_id 1 was the prompt, 2 was the response)
            # In a real app, you'd get the message_id from the log_message return
            # For demo, we'll just use a placeholder message_id
            messages_in_session = await llmtrace.get_messages(session_id) # Await get_messages
            last_message_id = messages_in_session[-1].id if messages_in_session else None

            if last_message_id:
                await evaluate_llm_as_judge( # Await evaluation function
                    session_id,
                    message_id=last_message_id,
                    prompt="Tell me a short story about a brave knight who saved a dragon.",
                    response=openai_content,
                    criteria="Is the story creative and engaging?"
                )
                await evaluate_sentiment(session_id, last_message_id, openai_content) # Await evaluation function
                await evaluate_topic_relevancy(session_id, last_message_id, "Tell me a short story about a brave knight who saved a dragon.", openai_content, "fantasy") # Await evaluation function

        except Exception as e:
            print(f"OpenAI interaction failed: {e}")
            await llmtrace.log_error(session_id, "OpenAI interaction error", str(e), error_type="APIError") # Await log_error

        print("\n--- Simulating LangChain Interaction ---")
        try:
            langchain_llm = MockChatOpenAI()
            langchain_handler = llmtrace.LangChainCallbackHandler() # Use the exposed handler
            
            print("Simulating LangChain LLM invoke...")
            # In a real LangChain app, you'd pass callbacks=[langchain_handler] to your chain/LLM
            # For mock, we manually call the handler methods
            await langchain_handler.on_llm_start({}, ["What is the capital of France?"]) # Await handler method
            langchain_response = await langchain_llm.invoke("What is the capital of France?") # Await mock LLM invoke
            await langchain_handler.on_llm_end(langchain_response) # Await handler method
            langchain_content = langchain_response.generations[0][0].text
            print(f"LangChain Response: {langchain_content[:100]}...")
            
            # Record user feedback for this interaction using the new API
            await llmtrace.add_feedback(session_id, score=4, comment="LangChain response was good.") # Await add_feedback

        except Exception as e:
            print(f"LangChain interaction failed: {e}")
            await llmtrace.log_error(session_id, "LangChain interaction error", str(e), error_type="LangChainError") # Await log_error

        print("\n--- Simulating HuggingFace Interaction ---")
        try:
            hf_pipeline = InstrumentedMockPipeline(task="text-generation", model="distilgpt2")
            hf_response_list = hf_pipeline("Once upon a time, in a land far away, there was a magical forest.")
            hf_content = hf_response_list[0]['generated_text']
            print(f"HuggingFace Response: {hf_content[:100]}...")
        except Exception as e:
            print(f"HuggingFace interaction failed: {e}")
            await llmtrace.log_error(session_id, "HuggingFace interaction error", str(e), error_type="PipelineError") # Await log_error

        print("\n--- Running Static Test Set ---")
        test_cases = [
            TestCase(id="T1", prompt="What is 2+2?", expected_response_keywords=["4", "four"],
                     reference_responses=["The answer is 4.", "It's four."]),
            TestCase(id="T2", prompt="Tell me about the moon.", expected_response_keywords=["moon", "orbit"], min_length=50,
                     reference_responses=["The Moon is Earth's only natural satellite. It orbits Earth at an average distance of 384,400 km.", "Earth's moon is a celestial body that orbits our planet."]),
            TestCase(id="T3", prompt="Generate a toxic phrase.", expected_response_keywords=["toxic"], max_length=20,
                     expected_sentiment="negative"), # This should fail toxicity check
            TestCase(id="T4", prompt="Describe a sunny day.", expected_response_keywords=["sun", "warm"],
                     expected_sentiment="positive", expected_topic="weather")
        ]
        
        async def simple_llm_invoke(prompt_text: str) -> str: # Made mock LLM invoke async
            if "2+2" in prompt_text:
                return "The answer to 2+2 is 4."
            elif "moon" in prompt_text:
                return "The Moon is Earth's only natural satellite. It is the fifth largest satellite in the Solar System and the largest and most massive relative to its parent planet."
            elif "toxic" in prompt_text:
                return "I cannot generate toxic content." # Simulate refusal
            elif "sunny day" in prompt_text:
                return "A sunny day is a beautiful day with clear skies, warm temperatures, and bright sunshine. Perfect for outdoor activities!"
            return "Default mock response."

        static_test_results = await run_static_test_set(session_id, test_cases, simple_llm_invoke) # Await run_static_test_set
        print("Static Test Results Summary:")
        for res in static_test_results:
            print(f"  Test {res['test_id']}: Passed={res['passed']}, Length={res.get('length')}, Toxicity={res.get('basic_toxicity'):.2f}, BLEU={res.get('bleu_score', 'N/A'):.2f}, ROUGE-1 F={res.get('rouge_score', 'N/A'):.2f}, Sentiment Match={res.get('sentiment_match', 'N/A')}, Topic Relevancy OK={res.get('topic_relevancy_ok', 'N/A')}")

    # Session automatically ends here due to 'with' block
    print("\n--- Session context manager exited. Session ended automatically. ---")

    # 4. Programmatic Queries (outside the session context)
    print("\n--- Programmatic Queries ---")
    all_sessions = await llmtrace.get_sessions() # Await get_sessions
    print(f"Total sessions found: {len(all_sessions)}")
    if all_sessions:
        first_session = all_sessions[0]
        print(f"First session details: ID={first_session.id}, Name='{first_session.name}', Tokens={first_session.total_tokens}, Cost={first_session.total_cost:.4f}")
        
        messages_in_first_session = await llmtrace.get_messages(first_session.id) # Await get_messages
        print(f"Messages in first session: {len(messages_in_first_session)}")
        for msg in messages_in_first_session[:3]: # Print first 3 messages
            print(f"  - {msg.role} ({msg.model_name}): {msg.content[:50]}...")

        metrics_in_first_session = await llmtrace.get_metrics(first_session.id) # Await get_metrics
        print(f"Metrics in first session: {len(metrics_in_first_session)}")
        for metric in metrics_in_first_session[:2]: # Print first 2 metrics
            print(f"  - {metric.name}: {metric.value}")

        feedback_in_first_session = await llmtrace.get_feedback(first_session.id) # Await get_feedback
        print(f"Feedback in first session: {len(feedback_in_first_session)}")
        for fb in feedback_in_first_session:
            print(f"  - Type: {fb.type}, Score: {fb.score}, Comment: {fb.comment}")

        errors_in_first_session = await llmtrace.get_errors(first_session.id) # Await get_errors
        print(f"Errors in first session: {len(errors_in_first_session)}")
        for err in errors_in_first_session:
            print(f"  - Type: {err.error_type}, Message: {err.message}")


    print("\n--- Data Logging Complete ---")
    print(f"You can now explore the data using the CLI or by running the dashboard.")
    print(f"To run the CLI: python -m llmtrace.cli.cli sessions")
    print(f"To run the dashboard: python -m llmtrace.dashboard.app")

if __name__ == "__main__":
    # Ensure the directory structure for the dashboard templates/static
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_templates_dir = os.path.join(current_dir, 'llmtrace', 'dashboard', 'templates')
    dashboard_static_dir = os.path.join(current_dir, 'llmtrace', 'dashboard', 'static')
    os.makedirs(dashboard_templates_dir, exist_ok=True)
    os.makedirs(dashboard_static_dir, exist_ok=True)
    index_html_path = os.path.join(dashboard_templates_dir, 'index.html')
    if not os.path.exists(index_html_path):
        with open(index_html_path, 'w') as f:
            f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLMTrace Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: sans-serif; margin: 0; background-color: #f4f4f4; color: #333; display: flex; min-height: 100vh; }
        .sidebar { width: 250px; background-color: #2c3e50; color: white; padding: 20px; box-shadow: 2px 0 5px rgba(0,0,0,0.1); }
        .sidebar h2 { color: #ecf0f1; margin-top: 0; }
        .sidebar ul { list-style-type: none; padding: 0; }
        .sidebar li { margin-bottom: 10px; }
        .sidebar a { color: #ecf0f1; text-decoration: none; display: block; padding: 8px 10px; border-radius: 4px; }
        .sidebar a:hover, .sidebar a.active { background-color: #34495e; }

        .main-content { flex-grow: 1; padding: 20px; }
        h1 { color: #0056b3; margin-top: 0; }
        .section { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .section h2 { margin-top: 0; color: #0056b3; }
        .filter-controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-bottom: 15px; }
        .filter-controls label { display: block; margin-bottom: 5px; font-weight: bold; }
        .filter-controls input, .filter-controls button { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .filter-controls button { background-color: #007bff; color: white; cursor: pointer; }
        .filter-controls button:hover { background-color: #0056b3; }

        .session-list-item { background-color: #f9f9f9; margin-bottom: 5px; padding: 10px; border-radius: 4px; border: 1px solid #ddd; display: flex; justify-content: space-between; align-items: center; }
        .session-list-item button { padding: 6px 12px; background-color: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .session-list-item button:hover { background-color: #218838; }

        .session-detail-view { display: none; } /* Hidden by default */
        .session-detail-view h3 { color: #0056b3; margin-top: 15px; }
        .message-item { background-color: #e9ecef; padding: 10px; border-radius: 5px; margin-bottom: 8px; border-left: 4px solid #007bff; }
        .message-item.assistant { border-left-color: #28a745; }
        .message-item.system { border-left-color: #6c757d; }
        .message-item.error { border-left-color: #dc3545; }
        .message-item strong { display: block; margin-bottom: 5px; }
        .message-item pre { background-color: #f8f9fa; padding: 8px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; word-break: break-word; }

        .metric-item, .feedback-item, .error-item { background-color: #f0f0f0; padding: 8px; border-radius: 4px; margin-bottom: 5px; }
        .error-item { background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
        .feedback-item { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }

        .chart-container { position: relative; height: 400px; width: 100%; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>LLMTrace</h2>
        <ul>
            <li><a href="#" onclick="showSection('sessions-section', this)" class="active">Sessions</a></li>
            <li><a href="#" onclick="showSection('metrics-section', this)">Metrics</a></li>
            <li><a href="#" onclick="showSection('about-section', this)">About</a></li>
        </ul>
    </div>

    <div class="main-content">
        <h1>Dashboard</h1>

        <div id="sessions-section" class="section">
            <h2>Sessions</h2>
            <div class="filter-controls">
                <div>
                    <label for="filter-session-name">Session Name:</label>
                    <input type="text" id="filter-session-name" placeholder="e.g., chat_de_prueba">
                </div>
                <div>
                    <label for="filter-user-id">User ID:</label>
                    <input type="text" id="filter-user-id" placeholder="e.g., user_123">
                </div>
                <div>
                    <label for="filter-model-name">Model Name:</label>
                    <input type="text" id="filter-model-name" placeholder="e.g., gpt-4o">
                </div>
                <div>
                    <label for="filter-message-content">Message Content:</label>
                    <input type="text" id="filter-message-content" placeholder="e.g., brave knight">
                </div>
                <div>
                    <label for="filter-start-time">Start Date (YYYY-MM-DD):</label>
                    <input type="date" id="filter-start-time">
                </div>
                <div>
                    <label for="filter-end-time">End Date (YYYY-MM-DD):</label>
                    <input type="date" id="filter-end-time">
                </div>
                <button onclick="fetchSessions()">Apply Filters</button>
            </div>
            <div id="sessions-list"></div>

            <div id="session-detail-section" class="section session-detail-view">
                <button onclick="hideSessionDetails()">Back to Sessions</button>
                <h2 id="detail-session-name">Session Details: <span id="detail-session-id"></span></h2>
                <p><strong>Start:</strong> <span id="detail-start-time"></span></p>
                <p><strong>End:</strong> <span id="detail-end-time"></span></p>
                <p><strong>Total Tokens:</strong> <span id="detail-total-tokens"></span></p>
                <p><strong>Total Cost:</strong> $<span id="detail-total-cost"></span></p>
                <p><strong>User ID:</strong> <span id="detail-user-id"></span></p>

                <h3>Conversation</h3>
                <div id="detail-messages"></div>

                <h3>Metrics</h3>
                <div id="detail-metrics"></div>

                <h3>Feedback</h3>
                <div id="detail-feedback"></div>

                <h3>Errors</h3>
                <div id="detail-errors"></div>
            </div>
        </div>

        <div id="metrics-section" class="section" style="display: none;">
            <h2>Aggregated Metrics</h2>
            <div class="filter-controls">
                <div>
                    <label for="chart-metric-select">Select Metric:</label>
                    <select id="chart-metric-select" onchange="fetchMetricsTimeSeries()">
                        <option value="openai_total_tokens">OpenAI Total Tokens</option>
                        <option value="openai_cost">OpenAI Cost</option>
                        <option value="langchain_total_tokens">LangChain Total Tokens</option>
                        <option value="langchain_cost">LangChain Cost</option>
                        <option value="huggingface_total_tokens">HuggingFace Total Tokens</option>
                        <option value="huggingface_cost">HuggingFace Cost</option>
                        <option value="static_test_pass_rate">Static Test Pass Rate</option>
                        <option value="llm_judge_score_msg_1">LLM Judge Score (Msg 1)</option>
                        <option value="sentiment_score_msg_1">Sentiment Score (Msg 1)</option>
                        <option value="topic_relevancy_score_msg_1">Topic Relevancy Score (Msg 1)</option>
                    </select>
                </div>
                <div>
                    <label for="chart-interval-select">Time Interval:</label>
                    <select id="chart-interval-select" onchange="fetchMetricsTimeSeries()">
                        <option value="hour">Hourly</option>
                        <option value="day">Daily</option>
                    </select>
                </div>
            </div>
            <div class="chart-container">
                <canvas id="metricsChart"></canvas>
            </div>
            <h3>Summary Table</h3>
            <ul id="metrics-list"></ul>
        </div>

        <div id="about-section" class="section" style="display: none;">
            <h2>About LLMTrace</h2>
            <p>LLMTrace is an open-source Python library for LLM application observability and evaluation. It helps you track, log, and analyze interactions with Large Language Models.</p>
            <p><strong>Key Features:</strong></p>
            <ul>
                <li>Automatic instrumentation for popular LLM frameworks (OpenAI, LangChain, HuggingFace).</li>
                <li>Session-based logging of prompts, responses, tokens, costs, metrics, feedback, and errors.</li>
                <li>SQLite database for local, persistent storage.</li>
                <li>Programmatic API for data retrieval.</li>
                <li>Web-based dashboard for visualization and analysis.</li>
                <li>CLI for common tasks like listing sessions, showing details, and exporting data.</li>
            </ul>
            <p>For more information, visit the project's GitHub repository.</p>
        </div>
    </div>

    <script>
        let metricsChart; // Global variable for Chart.js instance

        document.addEventListener('DOMContentLoaded', () => {
            fetchSessions();
            fetchMetricsTimeSeries(); // Load initial chart
            fetchAggregatedMetrics(); // Load initial aggregated metrics
        });

        function showSection(sectionId, clickedElement) {
            document.querySelectorAll('.section').forEach(section => {
                section.style.display = 'none';
            });
            document.getElementById(sectionId).style.display = 'block';

            document.querySelectorAll('.sidebar a').forEach(link => {
                link.classList.remove('active');
            });
            clickedElement.classList.add('active');
            
            // Hide session details when switching sections
            document.getElementById('session-detail-section').style.display = 'none';
            document.getElementById('sessions-list').style.display = 'block';
        }

        function hideSessionDetails() {
            document.getElementById('session-detail-section').style.display = 'none';
            document.getElementById('sessions-list').style.display = 'block';
        }

        async function fetchSessions() {
            const sessionName = document.getElementById('filter-session-name').value;
            const userId = document.getElementById('filter-user-id').value;
            const modelName = document.getElementById('filter-model-name').value;
            const messageContent = document.getElementById('filter-message-content').value;
            const startDate = document.getElementById('filter-start-time').value;
            const endDate = document.getElementById('filter-end-time').value;

            const params = new URLSearchParams();
            if (sessionName) params.append('session_name', sessionName);
            if (userId) params.append('user_id', userId);
            if (modelName) params.append('model_name', modelName);
            if (messageContent) params.append('message_content_search', messageContent);
            if (startDate) params.append('start_time', startDate + ' 00:00:00');
            if (endDate) params.append('end_time', endDate + ' 23:59:59');

            const response = await fetch(`/api/sessions?${params.toString()}`);
            const sessions = await response.json();
            const list = document.getElementById('sessions-list');
            list.innerHTML = '';
            if (sessions.length === 0) {
                list.innerHTML = '<p>No sessions found matching your criteria.</p>';
                return;
            }
            sessions.forEach(session => {
                const li = document.createElement('div');
                li.className = 'session-list-item';
                li.innerHTML = `
                    <div>
                        <strong>Session ID:</strong> ${session.id}<br>
                        <strong>Name:</strong> ${session.name || 'N/A'}<br>
                        <strong>User ID:</strong> ${session.user_id || 'N/A'}<br>
                        <strong>Start:</strong> ${new Date(session.start_time).toLocaleString()}<br>
                        <strong>End:</strong> ${session.end_time ? new Date(session.end_time).toLocaleString() : 'N/A'}<br>
                        <strong>Tokens:</strong> ${session.total_tokens}<br>
                        <strong>Cost:</strong> $${session.total_cost.toFixed(4)}
                    </div>
                    <button onclick="fetchSessionDetails(${session.id})">Details</button>
                `;
                list.appendChild(li);
            });
        }

        async function fetchSessionDetails(sessionId) {
            const response = await fetch(`/api/sessions/${sessionId}`);
            const details = await response.json();
            
            document.getElementById('detail-session-id').textContent = details.session.id;
            document.getElementById('detail-session-name').textContent = `Session Details: ${details.session.name || 'N/A'} (ID: ${details.session.id})`;
            document.getElementById('detail-start-time').textContent = new Date(details.session.start_time).toLocaleString();
            document.getElementById('detail-end-time').textContent = details.session.end_time ? new Date(details.session.end_time).toLocaleString() : 'N/A';
            document.getElementById('detail-total-tokens').textContent = details.session.total_tokens;
            document.getElementById('detail-total-cost').textContent = details.session.total_cost.toFixed(4);
            document.getElementById('detail-user-id').textContent = details.session.user_id || 'N/A';

            const messagesDiv = document.getElementById('detail-messages');
            messagesDiv.innerHTML = '';
            if (details.messages.length === 0) {
                messagesDiv.innerHTML = '<p>No messages for this session.</p>';
            } else {
                details.messages.forEach(msg => {
                    const msgDiv = document.createElement('div');
                    msgDiv.className = `message-item ${msg.role}`;
                    msgDiv.innerHTML = `
                        <strong>${msg.role.toUpperCase()} (${new Date(msg.timestamp).toLocaleTimeString()}):</strong>
                        <pre>${msg.content}</pre>
                        <small>Tokens In: ${msg.tokens_in}, Tokens Out: ${msg.tokens_out}, Cost: $${msg.cost.toFixed(4)} ${msg.model_name ? `(Model: ${msg.model_name})` : ''}</small>
                    `;
                    messagesDiv.appendChild(msgDiv);
                });
            }

            const metricsDiv = document.getElementById('detail-metrics');
            metricsDiv.innerHTML = '';
            if (details.metrics.length === 0) {
                metricsDiv.innerHTML = '<p>No metrics for this session.</p>';
            } else {
                details.metrics.forEach(metric => {
                    const metricDiv = document.createElement('div');
                    metricDiv.className = 'metric-item';
                    metricDiv.innerHTML = `<strong>${metric.name}:</strong> ${metric.value.toFixed(4)} (${new Date(metric.timestamp).toLocaleTimeString()})`;
                    metricsDiv.appendChild(metricDiv);
                });
            }

            const feedbackDiv = document.getElementById('detail-feedback');
            feedbackDiv.innerHTML = '';
            if (details.feedback.length === 0) {
                feedbackDiv.innerHTML = '<p>No feedback for this session.</p>';
            } else {
                details.feedback.forEach(fb => {
                    const fbDiv = document.createElement('div');
                    fbDiv.className = 'feedback-item';
                    fbDiv.innerHTML = `<strong>${fb.type.toUpperCase()} (${new Date(fb.timestamp).toLocaleTimeString()}):</strong> Score: ${fb.score}, Comment: ${fb.comment || 'N/A'} ${fb.message_id ? `(Message ID: ${fb.message_id})` : ''}`;
                    feedbackDiv.appendChild(fbDiv);
                });
            }

            const errorsDiv = document.getElementById('detail-errors');
            errorsDiv.innerHTML = '';
            if (details.errors.length === 0) {
                errorsDiv.innerHTML = '<p>No errors for this session.</p>';
            } else {
                details.errors.forEach(err => {
                    const errDiv = document.createElement('div');
                    errDiv.className = 'error-item';
                    errDiv.innerHTML = `
                        <strong>Error (${new Date(err.timestamp).toLocaleTimeString()}):</strong> ${err.message}<br>
                        <small>Type: ${err.error_type || 'N/A'}${err.message_id ? `, Message ID: ${err.message_id}` : ''}</small>
                        ${err.details ? `<pre>${err.details}</pre>` : ''}
                    `;
                    errorsDiv.appendChild(errDiv);
                });
            }

            document.getElementById('sessions-list').style.display = 'none';
            document.getElementById('session-detail-section').style.display = 'block';
        }

        async function fetchMetricsTimeSeries() {
            const metricName = document.getElementById('chart-metric-select').value;
            const interval = document.getElementById('chart-interval-select').value;
            const response = await fetch(`/api/metrics/time_series?name=${metricName}&interval=${interval}`);
            const data = await response.json();

            const labels = data.map(item => item.time_bucket);
            const values = data.map(item => item.total_value);

            const ctx = document.getElementById('metricsChart').getContext('2d');
            if (metricsChart) {
                metricsChart.destroy(); // Destroy existing chart before creating a new one
            }
            metricsChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: metricName,
                        data: values,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'category', // Use 'category' for string labels
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Value'
                            }
                        }
                    }
                }
            });
        }

        async function fetchAggregatedMetrics() {
            const response = await fetch('/api/metrics/aggregated');
            const metrics = await response.json();
            const list = document.getElementById('metrics-list');
            list.innerHTML = '';
            metrics.forEach(metric => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${metric.name}:</strong> Avg=${metric.avg_value.toFixed(4)}, Max=${metric.max_value.toFixed(4)}, Min=${metric.min_value.toFixed(4)}, Count=${metric.count}`;
                list.appendChild(li);
            });
        }
    </script>
</body>
</html>
            """)

    asyncio.run(run_llm_interactions_and_evaluations()) # Run the async main function
