"""Alembic configuration for database migrations."""
import os
from logging.config import fileConfig
from dotenv import load_dotenv
 
from sqlalchemy import create_engine
 
from alembic import context
 
# Load environment variables from .env file
load_dotenv()
 
# this is the Alembic Config object
config = context.config
 
# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
 
# add your model's MetaData object here
import sys
from pathlib import Path
 
# Ensure project root is on sys.path so `app` package can be imported when
# Alembic loads this env.py from the migrations directory.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
 
from app.core.database import Base
# Import models package so all model modules are loaded and registered with Base.metadata
import app.models  # noqa: F401
 
target_metadata = Base.metadata
 
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Use explicit IPv4 address to avoid IPv6 resolution issues on Windows
    # Default to host port 5433 which maps to the Postgres container's 5432 in docker-compose
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@127.0.0.1:5433/verifiable_stubs')
 
    # (Previously printed the database URL for debugging; removed.)
    connectable = create_engine(database_url, poolclass=None)
 
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
 
        with context.begin_transaction():
            context.run_migrations()
 
 
if context.is_offline_mode():
    raise RuntimeError("Offline mode not supported")
else:
    run_migrations_online()
 