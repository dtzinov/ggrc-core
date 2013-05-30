from __future__ import with_statement
from alembic import context
from logging.config import fileConfig

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Ensure all models are imported so they can be used
# with --autogenerate
from ggrc.app import db, app
from ggrc.models import all_models

target_metadata = db.metadata

def _get_db_scheme():
    """Returns the database type, e.g. 'sqlite' or 'mysql' based
    on the database URI.
    """
    url = app.config['SQLALCHEMY_DATABASE_URI']
    db_scheme = url.split(':')[0].split('+')[0]
    return db_scheme

def include_symbol(tablename, schema=None):
    """Exclude some tables from consideration by alembic's 'autogenerate'.
    """
    db_scheme = _get_db_scheme()

    # Exclude some tables when considering SQLite3, because full text search
    # generates tables that are not reflected in SQLAlchemy's metadata.
    sqlite_fts_exclusions = [
        # Exclude SQLite full-text-search tables
        'fulltext_record_properties_content',
        'fulltext_record_properties_docsize',
        'fulltext_record_properties_segdir',
        'fulltext_record_properties_segments',
        'fulltext_record_properties_stat',
        'fulltext_record_properties',
        ]

    if db_scheme == 'sqlite' and tablename in sqlite_fts_exclusions:
        return False

    # If the tablename didn't match any exclusion cases, return True
    return True

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        include_symbol=include_symbol)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    engine = db.engine

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_symbol=include_symbol)

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
