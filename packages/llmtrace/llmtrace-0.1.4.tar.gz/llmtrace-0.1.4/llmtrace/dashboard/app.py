"""
Web dashboard application for LLMTrace, built with Flask.

Provides routes for viewing sessions, messages, metrics, feedback, and errors,
along with aggregated statistics and time-series data. It serves as a graphical
interface for exploring the tracing data collected by LLMTrace.
"""

from flask import Flask, jsonify, render_template, request
from llmtrace.storage import get_storage_backend
from llmtrace.core.core import _db_instance
import os
from datetime import datetime, timedelta
import asyncio

def create_dashboard_app() -> Flask:
    """
    Factory function to create and configure the Flask dashboard application.

    Initializes the LLMTrace database connection if it hasn't been already,
    and sets up the Flask routes for serving the dashboard and its API endpoints.

    :returns: The configured Flask application instance.
    :rtype: Flask
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')

    if _db_instance is None:
        from llmtrace.core import core as llmtrace_core
        async def _init_db_for_flask():
            await llmtrace_core.init(db_path=os.path.expanduser('~/.llmtrace/llmtrace.db'))
            print("Dashboard: Initializing LLMTrace core for standalone use.")
        
        if not llmtrace_core._db_instance:
            asyncio.run(_init_db_for_flask())

    @app.route('/')
    async def index() -> str:
        """
        Renders the main dashboard HTML page.

        :returns: The rendered HTML content of the dashboard.
        :rtype: str
        """
        return render_template('index.html')

    @app.route('/api/sessions')
    async def get_sessions_api() -> jsonify:
        """
        API endpoint to retrieve a list of sessions, with optional filtering.

        Allows filtering by time range, session name, user ID, message content,
        model name, and total tokens/cost.

        :queryparam start_time: Filter sessions starting after this time (ISO format).
        :querytype start_time: str
        :queryparam end_time: Filter sessions ending before this time (ISO format).
        :querytype end_time: str
        :queryparam session_name: Filter sessions by name (partial match).
        :querytype session_name: str
        :queryparam user_id: Filter sessions by user ID (partial match).
        :querytype user_id: str
        :queryparam message_content_search: Filter sessions by content in their messages (partial match).
        :querytype message_content_search: str
        :queryparam model_name: Filter sessions by model name used in messages (partial match).
        :querytype model_name: str
        :queryparam min_tokens: Filter sessions with total_tokens >= this value.
        :querytype min_tokens: int
        :queryparam max_tokens: Filter sessions with total_tokens <= this value.
        :querytype max_tokens: int
        :queryparam min_cost: Filter sessions with total_cost >= this value.
        :querytype min_cost: float
        :queryparam max_cost: Filter sessions with total_cost <= this value.
        :querytype max_cost: float
        :returns: A JSON array of session dictionaries.
        :rtype: jsonify
        """
        db = _db_instance
        if not db:
            return jsonify({"error": "Database not initialized"}), 500
        
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        session_name = request.args.get('session_name')
        user_id = request.args.get('user_id')
        message_content_search = request.args.get('message_content_search')
        model_name = request.args.get('model_name')
        min_tokens = request.args.get('min_tokens', type=int)
        max_tokens = request.args.get('max_tokens', type=int)
        min_cost = request.args.get('min_cost', type=float)
        max_cost = request.args.get('max_cost', type=float)

        sessions = await db.get_filtered_sessions(
            start_time=start_time,
            end_time=end_time,
            session_name=session_name,
            user_id=user_id,
            message_content_search=message_content_search,
            model_name=model_name,
            min_tokens=min_tokens,
            max_tokens=max_tokens,
            min_cost=min_cost,
            max_cost=max_cost
        )
        return jsonify([s.to_dict() for s in sessions])

    @app.route('/api/sessions/<int:session_id>')
    async def get_session_details_api(session_id: int) -> jsonify:
        """
        API endpoint to retrieve detailed information for a specific session.

        Includes session metadata, messages, metrics, feedback, and errors associated
        with the given session ID.

        :param session_id: The ID of the session to retrieve.
        :type session_id: int
        :returns: A JSON object containing session details and related data.
        :rtype: jsonify
        :status 404: If the session is not found.
        :status 500: If the database is not initialized.
        """
        db = _db_instance
        if not db:
            return jsonify({"error": "Database not initialized"}), 500
        
        session = await db.get_session(session_id)
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        messages = await db.get_messages_for_session(session_id)
        metrics = await db.get_metrics_for_session(session_id)
        feedback = await db.get_feedback_for_session(session_id)
        errors = await db.get_errors_for_session(session_id)

        return jsonify({
            "session": session.to_dict(),
            "messages": [m.to_dict() for m in messages],
            "metrics": [m.to_dict() for m in metrics],
            "feedback": [f.to_dict() for f in feedback],
            "errors": [e.to_dict() for e in errors],
        })

    @app.route('/api/metrics/time_series')
    async def get_metrics_time_series_api() -> jsonify:
        """
        API endpoint to retrieve time-series data for a specific metric.

        Aggregates metric values by a specified time interval (hourly or daily)
        and allows filtering by date range.

        :queryparam name: The name of the metric (e.g., 'openai_total_tokens'). Defaults to 'openai_total_tokens'.
        :querytype name: str
        :queryparam interval: The time aggregation interval ('hour', 'day'). Defaults to 'hour'.
        :querytype interval: str
        :queryparam start_date: Filter data starting after this date (YYYY-MM-DD). Defaults to None.
        :querytype start_date: str
        :queryparam end_date: Filter data ending before this date (YYYY-MM-DD). Defaults to None.
        :querytype end_date: str
        :returns: A JSON array of dictionaries with time buckets and aggregated values.
        :rtype: jsonify
        :status 500: If the database is not initialized.
        """
        db = _db_instance
        if not db:
            return jsonify({"error": "Database not initialized"}), 500
        
        metric_name = request.args.get('name', 'openai_total_tokens')
        interval = request.args.get('interval', 'hour')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        time_series_data = await db.get_metrics_time_series(metric_name, interval, start_date, end_date)
        return jsonify(time_series_data)

    @app.route('/api/metrics/aggregated')
    async def get_aggregated_metrics_api() -> jsonify:
        """
        API endpoint to retrieve overall aggregated metrics summary.

        Provides high-level statistics across all sessions, such as total sessions,
        total tokens, total cost, average values, error rates, top error types,
        and top models by usage.

        :returns: A JSON object containing various aggregated metrics.
        :rtype: jsonify
        :status 500: If the database is not initialized.
        """
        db = _db_instance
        if not db:
            return jsonify({"error": "Database not initialized"}), 500
        
        summary = await db.get_overall_metrics_summary()
        return jsonify(summary)

    @app.route('/api/metrics/model_usage')
    async def get_model_usage_api() -> jsonify:
        """
        API endpoint to retrieve aggregated token usage per model.

        Provides a breakdown of total tokens consumed by each LLM model used.

        :returns: A JSON array of dictionaries with model names and their total token usage.
        :rtype: jsonify
        :status 500: If the database is not initialized.
        """
        db = _db_instance
        if not db:
            return jsonify({"error": "Database not initialized"}), 500
        
        model_usage_data = await db.get_model_token_usage()
        return jsonify(model_usage_data)

    @app.route('/api/metrics/feedback_distribution')
    async def get_feedback_distribution_api() -> jsonify:
        """
        API endpoint to retrieve the distribution of feedback scores.

        Provides counts for each distinct feedback score (e.g., how many 1-star, 2-star ratings).

        :returns: A JSON array of dictionaries with score and count.
        :rtype: jsonify
        :status 500: If the database is not initialized.
        """
        db = _db_instance
        if not db:
            return jsonify({"error": "Database not initialized"}), 500
        
        feedback_data = await db.get_feedback_score_distribution()
        return jsonify(feedback_data)

    @app.route('/api/metrics/error_types')
    async def get_error_types_api() -> jsonify:
        """
        API endpoint to retrieve the counts of different error types.

        Provides a breakdown of how many times each error type has occurred.

        :returns: A JSON array of dictionaries with error type and count.
        :rtype: jsonify
        :status 500: If the database is not initialized.
        """
        db = _db_instance
        if not db:
            return jsonify({"error": "Database not initialized"}), 500
        
        error_data = await db.get_error_type_counts()
        return jsonify(error_data)

    @app.route('/api/metrics/session_duration_avg')
    async def get_avg_session_duration_api() -> jsonify:
        """
        API endpoint to retrieve the average session duration.

        Calculates the average duration of all completed sessions in seconds.

        :returns: A JSON object with the average session duration in seconds.
        :rtype: jsonify
        :status 500: If the database is not initialized.
        """
        db = _db_instance
        if not db:
            return jsonify({"error": "Database not initialized"}), 500
        
        avg_duration = await db.get_avg_session_duration()
        return jsonify({"avg_session_duration_seconds": avg_duration})

    return app

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(current_dir, 'templates')
    static_dir = os.path.join(current_dir, 'static')
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)

    app = create_dashboard_app()
    print("Note: Running Flask with async routes requires an ASGI server for production. Using Flask's built-in server for development.")
    app.run(debug=True, port=5000)
