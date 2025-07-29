"""
Initial database schema for LLMTrace.

Revision ID: 20240101_initial_schema
Revises:
Create Date: 2024-01-01 10:00:00.000000

This migration script creates the initial tables for LLMTrace:
- `sessions`: Stores information about LLM interaction sessions.
- `messages`: Stores individual messages (prompts/responses) within sessions.
- `metrics`: Stores performance and usage metrics for messages.
- `feedback`: Stores user feedback on messages.
- `errors`: Stores error information related to LLM interactions.

It also defines primary keys, foreign keys, and indexes with a consistent naming convention.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20240101_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Applies the initial database schema.
    """
    # Table: sessions
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('app_name', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_sessions_id'))
    )
    op.create_index(op.f('ix_sessions_app_name'), 'sessions', ['app_name'], unique=False)
    op.create_index(op.f('ix_sessions_user_id'), 'sessions', ['user_id'], unique=False)
    op.create_index(op.f('ix_sessions_start_time'), 'sessions', ['start_time'], unique=False)

    # Table: messages
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('model', sa.String(), nullable=True),
        sa.Column('prompt_tokens', sa.Integer(), nullable=True),
        sa.Column('completion_tokens', sa.Integer(), nullable=True),
        sa.Column('total_tokens', sa.Integer(), nullable=True),
        sa.Column('cost', sa.Float(), nullable=True),
        sa.Column('latency_ms', sa.Integer(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_messages_id')),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], name=op.f('fk_messages_session_id'), ondelete='CASCADE')
    )
    op.create_index(op.f('ix_messages_session_id'), 'messages', ['session_id'], unique=False)
    op.create_index(op.f('ix_messages_timestamp'), 'messages', ['timestamp'], unique=False)
    op.create_index(op.f('ix_messages_model'), 'messages', ['model'], unique=False)

    # Table: metrics
    op.create_table(
        'metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_metrics_id')),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], name=op.f('fk_metrics_session_id'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], name=op.f('fk_metrics_message_id'), ondelete='CASCADE')
    )
    op.create_index(op.f('ix_metrics_session_id'), 'metrics', ['session_id'], unique=False)
    op.create_index(op.f('ix_metrics_message_id'), 'metrics', ['message_id'], unique=False)
    op.create_index(op.f('ix_metrics_name'), 'metrics', ['name'], unique=False)

    # Table: feedback
    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('feedback_type', sa.String(), nullable=False), # e.g., 'rating', 'thumb_up', 'thumb_down'
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_feedback_id')),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], name=op.f('fk_feedback_session_id'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], name=op.f('fk_feedback_message_id'), ondelete='CASCADE')
    )
    op.create_index(op.f('ix_feedback_session_id'), 'feedback', ['session_id'], unique=False)
    op.create_index(op.f('ix_feedback_message_id'), 'feedback', ['message_id'], unique=False)
    op.create_index(op.f('ix_feedback_type'), 'feedback', ['feedback_type'], unique=False)

    # Table: errors
    op.create_table(
        'errors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=True),
        sa.Column('error_type', sa.String(), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('stacktrace', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_errors_id')),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], name=op.f('fk_errors_session_id'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], name=op.f('fk_errors_message_id'), ondelete='CASCADE')
    )
    op.create_index(op.f('ix_errors_session_id'), 'errors', ['session_id'], unique=False)
    op.create_index(op.f('ix_errors_message_id'), 'errors', ['message_id'], unique=False)
    op.create_index(op.f('ix_errors_type'), 'errors', ['error_type'], unique=False)


def downgrade() -> None:
    """
    Reverts the initial database schema.
    """
    op.drop_table('errors')
    op.drop_table('feedback')
    op.drop_table('metrics')
    op.drop_table('messages')
    op.drop_table('sessions')
