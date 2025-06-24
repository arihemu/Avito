from __future__ import annotations

import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .core.avito_client import AvitoClient
from .services.bump_service import BumpService
from .services.description_service import DescriptionService
from .services.stats_service import StatsService


def create_scheduler() -> AsyncIOScheduler:
    database_url = os.getenv("DATABASE_URL", "")
    jobstores = {
        "default": SQLAlchemyJobStore(url=database_url),
    }
    scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="Europe/Moscow")
    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    client = AvitoClient()

    async def collect_stats() -> None:
        async with session_factory() as session:
            service = StatsService(client, session)
            await service.collect_daily_views()

    async def monitor_competitors() -> None:
        ids = os.getenv("COMPETITOR_ITEM_IDS", "").split(",")
        competitor_ids = [int(i) for i in ids if i]
        async with session_factory() as session:
            service = DescriptionService(client, session)
            await service.monitor_competitors(competitor_ids)

    async def bump_top9() -> None:
        async with session_factory() as session:
            service = BumpService(client, session)
            await service.bump_top9()

    scheduler.add_job(collect_stats, "cron", hour=23, minute=0)
    scheduler.add_job(monitor_competitors, "cron", hour=0, minute=30)
    scheduler.add_job(bump_top9, "cron", hour=9, minute=0)
    return scheduler
