"""
Command Line Interface (CLI) for LLMTrace.

Provides tools to manage, view, export, and analyze LLM tracing data
directly from the terminal. This includes listing sessions, showing
detailed session information, exporting data, and running the web dashboard.
"""

import argparse
import json
import csv
import os
import webbrowser
import asyncio
from llmtrace.core import core
from llmtrace.storage import get_storage_backend
from llmtrace.dashboard.app import create_dashboard_app
from datetime import datetime

async def init_db_for_cli() -> None:
    """
    Initializes the LLMTrace database for CLI operations if not already done.

    Ensures that the global database instance (`core._db_instance`) is set up
    before any CLI command attempts to interact with the database.
    """
    if core._db_instance is None:
        await core.init(db_path=os.path.expanduser('~/.llmtrace/llmtrace.db'))

async def list_sessions(args: argparse.Namespace) -> None:
    """
    Lists all tracing sessions with summary information.

    Displays session ID, name, user ID, start/end times, total tokens, and total cost
    in a formatted table.

    :param args: An argparse Namespace object containing CLI arguments.
    :type args: argparse.Namespace
    """
    await init_db_for_cli()
    db = core._db_instance
    if not db:
        print("Error: LLMTrace database not initialized.")
        return

    sessions = await db.get_all_sessions()
    if not sessions:
        print("No sessions found.")
        return

    print(f"{'ID':<5} {'Name':<20} {'User ID':<10} {'Start Time':<25} {'End Time':<25} {'Tokens':<10} {'Cost':<10}")
    print("-" * 115)
    for s in sessions:
        start_time_str = s.start_time.strftime("%Y-%m-%d %H:%M:%S") if s.start_time else "N/A"
        end_time_str = s.end_time.strftime("%Y-%m-%d %H:%M:%S") if s.end_time else "N/A"
        print(f"{s.id:<5} {s.name if s.name else 'N/A':<20} {s.user_id if s.user_id else 'N/A':<10} {start_time_str:<25} {end_time_str:<25} {s.total_tokens:<10} {s.total_cost:<10.4f}")

async def show_session(args: argparse.Namespace) -> None:
    """
    Shows detailed information for a specific tracing session.

    Includes session metadata, a chronological list of messages (prompts and responses),
    logged metrics, user feedback, and any recorded errors.

    :param args: An argparse Namespace object containing CLI arguments, including 'session_id'.
    :type args: argparse.Namespace
    """
    await init_db_for_cli()
    db = core._db_instance
    if not db:
        print("Error: LLMTrace database not initialized.")
        return

    session_id = args.session_id
    session = await db.get_session(session_id)
    if not session:
        print(f"Session with ID {session_id} not found.")
        return

    print(f"\n--- Session Details (ID: {session.id}) ---")
    print(f"Name: {session.name if session.name else 'N/A'}")
    print(f"User ID: {session.user_id if session.user_id else 'N/A'}")
    print(f"Start Time: {session.start_time}")
    print(f"End Time: {session.end_time if session.end_time else 'N/A'}")
    print(f"Total Tokens: {session.total_tokens}")
    print(f"Total Cost: {session.total_cost:.4f}")

    messages = await db.get_messages_for_session(session_id)
    print("\n--- Messages ---")
    if messages:
        for msg in messages:
            print(f"[{msg.timestamp.strftime('%H:%M:%S')}] {msg.role.upper()} (Model: {msg.model_name if msg.model_name else 'N/A'}):")
            print(f"  Content: {msg.content[:150]}{'...' if len(msg.content) > 150 else ''}")
            print(f"  Tokens In/Out: {msg.tokens_in}/{msg.tokens_out}, Cost: {msg.cost:.4f}")
            print("-" * 30)
    else:
        print("No messages for this session.")

    metrics = await db.get_metrics_for_session(session_id)
    print("\n--- Metrics ---")
    if metrics:
        for metric in metrics:
            print(f"[{metric.timestamp.strftime('%H:%M:%S')}] {metric.name}: {metric.value}")
    else:
        print("No metrics for this session.")

    feedback = await db.get_feedback_for_session(session_id)
    print("\n--- Feedback ---")
    if feedback:
        for fb in feedback:
            print(f"[{fb.timestamp.strftime('%H:%M:%S')}] Type: {fb.type}, Score: {fb.score}, Message ID: {fb.message_id if fb.message_id else 'N/A'}, Comment: {fb.comment if fb.comment else 'N/A'}")
    else:
        print("No feedback for this session.")

    errors = await db.get_errors_for_session(session_id)
    print("\n--- Errors ---")
    if errors:
        for err in errors:
            print(f"[{err.timestamp.strftime('%H:%M:%S')}] Error Type: {err.error_type if err.error_type else 'N/A'}, Message: {err.message}")
            if err.details:
                print(f"  Details: {err.details}")
            if err.message_id:
                print(f"  Message ID: {err.message_id}")
    else:
        print("No errors for this session.")

async def export_data(args: argparse.Namespace) -> None:
    """
    Exports tracing data to a specified format (JSON or CSV).

    Can export all data or filter by a specific session ID.
    JSON export includes full nested data (sessions, messages, metrics, feedback, errors).
    CSV export is currently limited to session-level data.

    :param args: An argparse Namespace object containing CLI arguments,
                  including 'format', 'output', and optional 'id'.
    :type args: argparse.Namespace
    """
    await init_db_for_cli()
    db = core._db_instance
    if not db:
        print("Error: LLMTrace database not initialized.")
        return

    if args.id:
        session_to_export = await db.get_session(args.id)
        sessions_to_export = [session_to_export] if session_to_export else []
        if not sessions_to_export:
            print(f"Session with ID {args.id} not found. Nothing to export.")
            return
    else:
        sessions_to_export = await db.get_all_sessions()

    if not sessions_to_export:
        print("No data to export.")
        return

    data_to_export = []
    for session in sessions_to_export:
        if session:
            session_dict = session.to_dict()
            session_dict["messages"] = [m.to_dict() for m in await db.get_messages_for_session(session.id)]
            session_dict["metrics"] = [m.to_dict() for m in await db.get_metrics_for_session(session.id)]
            session_dict["feedback"] = [f.to_dict() for f in await db.get_feedback_for_session(session.id)]
            session_dict["errors"] = [e.to_dict() for e in await db.get_errors_for_session(session.id)]
            data_to_export.append(session_dict)

    output_file = args.output
    if not output_file:
        output_file = f"llmtrace_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if args.format == 'json':
            output_file += ".json"
        elif args.format == 'csv':
            output_file += ".csv"

    if args.format == 'json':
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_export, f, ensure_ascii=False, indent=4)
        print(f"Data exported to {output_file}")
    elif args.format == 'csv':
        print("Warning: CSV export currently only includes session-level data. For full data, use JSON format.")
        
        fieldnames = ['id', 'name', 'user_id', 'start_time', 'end_time', 'total_tokens', 'total_cost']
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for session_data in data_to_export:
                writer.writerow({k: session_data[k] for k in fieldnames})
        print(f"Session data exported to {output_file}")
    else:
        print("Unsupported format. Please choose 'json' or 'csv'.")

async def delete_session_cli(args: argparse.Namespace) -> None:
    """
    Deletes a specific tracing session and all its associated data.

    This action is irreversible and will remove all messages, metrics,
    feedback, and errors linked to the specified session ID.

    :param args: An argparse Namespace object containing CLI arguments, including 'session_id'.
    :type args: argparse.Namespace
    """
    await init_db_for_cli()
    db = core._db_instance
    if not db:
        print("Error: LLMTrace database not initialized.")
        return
    
    session_id = args.session_id
    session = await db.get_session(session_id)
    if not session:
        print(f"Session with ID {session_id} not found.")
        return

    confirm = input(f"Are you sure you want to delete session {session_id} and all its associated data? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            await db.delete_session(session_id)
            print(f"Session {session_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting session {session_id}: {e}")
    else:
        print("Deletion cancelled.")

async def purge_data(args: argparse.Namespace) -> None:
    """
    Purges all LLMTrace data from the database. This action is irreversible.

    This command will attempt to delete all records across all tables managed by LLMTrace.
    It requires confirmation from the user.

    :param args: An argparse Namespace object (no specific arguments used).
    :type args: argparse.Namespace
    """
    await init_db_for_cli()
    db = core._db_instance
    if not db:
        print("Error: LLMTrace database not initialized.")
        return

    confirm = input("Are you sure you want to purge ALL LLMTrace data? This action cannot be undone. (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            # This method needs to be implemented in the StorageBackend if not already.
            # For now, we'll simulate or add a direct purge method to backend.
            # A robust implementation would drop and recreate tables or truncate them.
            if hasattr(db, '_purge_all_data'): # Assuming a private method for full purge
                await db._purge_all_data()
                print("All LLMTrace data purged successfully.")
            else:
                # Fallback for backends without _purge_all_data
                print("Purge not fully supported by current backend. Attempting to delete all sessions...")
                all_sessions = await db.get_all_sessions()
                for s in all_sessions:
                    await db.delete_session(s.id)
                print("All sessions and associated data deleted. Note: Some tables might remain if not empty.")

        except Exception as e:
            print(f"Error purging data: {e}")
    else:
        print("Data purge cancelled.")

async def show_metrics_summary(args: argparse.Namespace) -> None:
    """
    Displays an overall aggregated metrics summary for all LLMTrace data.

    Provides high-level statistics such as total sessions, messages, tokens, cost,
    average values, error rates, top error types, and top models by usage.

    :param args: An argparse Namespace object (no specific arguments used).
    :type args: argparse.Namespace
    """
    await init_db_for_cli()
    db = core._db_instance
    if not db:
        print("Error: LLMTrace database not initialized.")
        return
    
    summary = await db.get_overall_metrics_summary()

    print("\n--- LLMTrace Overall Metrics Summary ---")
    print(f"Total Sessions: {summary.get('total_sessions', 0)}")
    print(f"Total Messages: {summary.get('total_messages', 0)}")
    print(f"Overall Tokens Used: {summary.get('total_tokens_overall', 0)}")
    print(f"Overall Estimated Cost: ${summary.get('total_cost_overall', 0.0):.4f}")
    print(f"Average Tokens per Session: {summary.get('avg_tokens_per_session', 0.0):.2f}")
    print(f"Average Cost per Session: ${summary.get('avg_cost_per_session', 0.0):.4f}")
    print(f"Session Error Rate: {summary.get('error_rate_sessions', 0.0):.2f}%")
    print(f"Average Feedback Score (Ratings): {summary.get('avg_feedback_score', 'N/A')}")

    print("\nTop 3 Error Types:")
    if summary.get('top_error_types'):
        for err_type in summary['top_error_types']:
            print(f"  - {err_type['error_type'] if err_type['error_type'] else 'N/A'}: {err_type['count']} occurrences")
    else:
        print("  No errors recorded.")

    print("\nTop 3 Models by Token Usage:")
    if summary.get('top_models_by_tokens'):
        for model_data in summary['top_models_by_tokens']:
            print(f"  - {model_data['model_name']}: {model_data['total_tokens']} tokens")
    else:
        print("  No model usage recorded.")
    print("-" * 40)

async def run_dashboard(args: argparse.Namespace) -> None:
    """
    Starts the LLMTrace web dashboard.

    This command launches a Flask web server that provides a graphical interface
    for exploring and analyzing LLMTrace data. It can optionally open the dashboard
    in the default web browser.

    :param args: An argparse Namespace object containing CLI arguments,
                  including 'port' and 'open_browser'.
    :type args: argparse.Namespace
    """
    await init_db_for_cli()
    app = create_dashboard_app()
    port = args.port
    print(f"Starting LLMTrace dashboard on http://127.0.0.1:{port}")
    if args.open_browser:
        webbrowser.open_new_tab(f"http://127.0.0.1:{port}")
    
    # Flask's app.run is synchronous. For true async, an ASGI server like uvicorn/hypercorn is needed.
    # For CLI demo purposes, we'll keep app.run, but note the async nature of API calls.
    print("Note: Flask's development server (app.run) is synchronous. For production, use an ASGI server like Gunicorn with Uvicorn workers.")
    app.run(debug=True, port=port)

def main():
    """
    Main entry point for the LLMTrace CLI.

    Parses command-line arguments and dispatches to the appropriate asynchronous function.
    """
    parser = argparse.ArgumentParser(description="LLMTrace CLI for observability and evaluation.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    parser_sessions = subparsers.add_parser('sessions', help='List all tracing sessions.')
    parser_sessions.set_defaults(func=list_sessions)

    parser_show = subparsers.add_parser('show', help='Show details of a specific session.')
    parser_show.add_argument('session_id', type=int, help='The ID of the session to show.')
    parser_show.set_defaults(func=show_session)

    parser_export = subparsers.add_parser('export', help='Export all tracing data.')
    parser_export.add_argument('--format', '-f', choices=['json', 'csv'], default='json',
                               help='Output format (json or csv).')
    parser_export.add_argument('--output', '-o', help='Output file path. Defaults to llmtrace_export_TIMESTAMP.json/csv.')
    parser_export.add_argument('--id', type=int, help='Export data for a specific session ID.')
    parser_export.set_defaults(func=export_data)

    parser_delete = subparsers.add_parser('delete', help='Delete a specific tracing session and its data.')
    parser_delete.add_argument('session_id', type=int, help='The ID of the session to delete.')
    parser_delete.set_defaults(func=delete_session_cli)

    parser_purge = subparsers.add_parser('purge', help='Purge all LLMTrace data from the database.')
    parser_purge.set_defaults(func=purge_data)

    parser_metrics = subparsers.add_parser('metrics', help='Show overall aggregated metrics.')
    parser_metrics.set_defaults(func=show_metrics_summary)

    parser_web = subparsers.add_parser('web', help='Start the LLMTrace web dashboard.')
    parser_web.add_argument('--port', '-p', type=int, default=5000, help='Port to run the dashboard on.')
    parser_web.add_argument('--no-browser', action='store_false', dest='open_browser', default=True,
                            help='Do not open the dashboard in a web browser automatically.')
    parser_web.set_defaults(func=run_dashboard)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        asyncio.run(args.func(args))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
