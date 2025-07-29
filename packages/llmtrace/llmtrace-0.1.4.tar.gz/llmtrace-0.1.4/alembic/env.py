import asyncio
from logging.config import fileConfig
import logging # Importar logging

from alembic import context

# Import your StorageBackend and specific backends
from llmtrace.storage import get_storage_backend
from llmtrace.storage.backends import StorageBackend

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env") # Logger específico para env.py

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import Base
# target_metadata = Base.metadata
# Since LLMTrace uses direct SQL for schema, we don't have a MetaData object.
# We will manage migrations manually.
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # For offline mode, you might still need to know the backend type
    # or provide a dummy URL. This is less common for async backends.
    # For simplicity, we'll focus on online mode.
    logger.warning("Offline migrations are not fully supported for async backends without a custom setup.")
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_name='sqlite' if url and 'sqlite' in url else 'postgresql', # Infer dialect
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """
    Runs migrations in 'online' mode.
    """
    # Define a naming convention for constraints (example for PostgreSQL)
    # This is a common practice to ensure consistent naming for indexes, foreign keys, etc.
    # For raw SQL migrations, you'd apply this convention when writing the SQL.
    # Example: "ix_%(column_0_label)s" for indexes, "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s" for foreign keys
    # Since we are doing manual migrations, this is more of a guideline for the SQL itself.
    
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_name='sqlite' if 'sqlite' in config.get_main_option("sqlalchemy.url", "") else 'postgresql',
        # Compare the current database schema against the target_metadata.
        # Since target_metadata is None, autogenerate won't work.
        # We will write manual migrations.
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    db_url = config.get_main_option("sqlalchemy.url")
    if not db_url:
        raise ValueError("Database URL not found in alembic.ini. Please set 'sqlalchemy.url'.")

    backend_type = None
    backend_kwargs = {}

    if db_url.startswith("sqlite:///"):
        backend_type = "sqlite"
        db_path = db_url.replace("sqlite:///", "")
        backend_kwargs = {"db_path": db_path}
    elif db_url.startswith("postgresql+asyncpg://"):
        backend_type = "postgresql"
        backend_kwargs = {"connection_string": db_url.replace("postgresql+asyncpg://", "postgresql://")}
    elif db_url == "memory://": # Soporte para DB en memoria para tests
        backend_type = "sqlite"
        backend_kwargs = {"db_path": ":memory:"}
    else:
        raise ValueError(f"Unsupported database URL scheme: {db_url}")

    logger.info(f"Running migrations online for backend: {backend_type} with URL: {db_url}")
    storage_backend: StorageBackend = await get_storage_backend(backend_type=backend_type, **backend_kwargs)
    
    await storage_backend.connect()
    
    try:
        connection = storage_backend._connection # Acceder a la conexión subyacente
        do_run_migrations(connection)
    finally:
        await storage_backend.close()
        logger.info("Database connection closed after migrations.")


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
