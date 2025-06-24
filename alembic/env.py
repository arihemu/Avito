from __future__ import annotations

import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context

from avito_helper.app.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

DATABASE_URL = os.getenv("DATABASE_URL")


def run_migrations_online() -> None:
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async def run_migrations(connection: Connection) -> None:
        await connection.run_sync(target_metadata.create_all)
        context.configure(connection=connection, target_metadata=target_metadata)
        await context.run_migrations()

    async with connectable.connect() as connection:
        await connection.run_sync(run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    raise RuntimeError("Offline mode not supported")
else:
    asyncio.run(run_migrations_online())
