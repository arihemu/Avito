from __future__ import annotations

import asyncio
import os

import typer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .core.avito_client import AvitoClient
from .scheduler import create_scheduler
from .services.bump_service import BumpService
from .services.description_service import DescriptionService
from .services.stats_service import StatsService


app = typer.Typer(add_completion=False)


def get_session_factory():
    database_url = os.getenv("DATABASE_URL")
    engine = create_async_engine(database_url)
    return async_sessionmaker(engine, expire_on_commit=False)


@app.command()
def run_scheduler() -> None:
    scheduler = create_scheduler()
    scheduler.start()
    typer.echo("Scheduler started")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        scheduler.shutdown()


@app.command()
async def collect_views() -> None:
    async with get_session_factory()() as session:
        service = StatsService(AvitoClient(), session)
        await service.collect_daily_views()


@app.command()
async def monitor_competitors() -> None:
    ids = os.getenv("COMPETITOR_ITEM_IDS", "").split(",")
    competitor_ids = [int(i) for i in ids if i]
    async with get_session_factory()() as session:
        service = DescriptionService(AvitoClient(), session)
        await service.monitor_competitors(competitor_ids)


@app.command()
async def bump_top9() -> None:
    async with get_session_factory()() as session:
        service = BumpService(AvitoClient(), session)
        await service.bump_top9()


if __name__ == "__main__":
    app()
