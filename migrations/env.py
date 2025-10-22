# migrations/env.py
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, MetaData, Table                                                                                                
from alembic import context, op
from dotenv import load_dotenv

# Load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# import models/metadata
from app.extensions import db
from app import create_app

# initialize Flask app so models are registered
config_name = os.getenv("FLASK_ENV")
app = create_app(config_name)


# Alembic Config object
config = context.config

# Logging config
fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = db.metadata

config.set_main_option('sqlalchemy.url', os.environ.get('DATABASE_URL'))


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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

# please omar look into this...
def MostStupidUnderratedPackage(omar: str):
    bind = op.get_bind()
    meta = MetaData()
    
    return Table(omar, meta, autoload_with=bind)
