from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Import our configuration and models - use lazy functions to avoid engine creation
from api.config import settings
from api.database import get_base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add our model's MetaData object here
# for 'autogenerate' support
target_metadata = get_base().metadata


def _fix_driver_in_url(db_url):
    """Ensure PostgreSQL URLs use psycopg2 driver explicitly for Vercel."""
    if db_url.startswith("postgresql://"):
        return db_url.replace("postgresql://", "postgresql+psycopg2://")
    elif db_url.startswith("postgres://"):
        return db_url.replace("postgres://", "postgresql+psycopg2://")
    return db_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = _fix_driver_in_url(settings.database_url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use DATABASE_URL from settings
    url = _fix_driver_in_url(settings.database_url)
    connectable = engine_from_config(
        {"sqlalchemy.url": url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
