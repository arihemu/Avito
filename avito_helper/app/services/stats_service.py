from __future__ import annotations

import datetime as dt
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.avito_client import AvitoClient
from ..models import Item, Stat


class StatsService:
    def __init__(self, client: AvitoClient, session: AsyncSession) -> None:
        self.client = client
        self.session = session

    async def collect_daily_views(self) -> None:
        resp = self.client.get("/stats/items")
        data = resp.json()
        today = dt.date.today()
        for entry in data.get("result", []):
            item_id = entry["item_id"]
            views = entry.get("unique_views", 0)
            stat = Stat(item_id=item_id, date=today, views_total=views)
            self.session.add(stat)
        await self.session.commit()

    async def top_items(self, days: int = 7, limit: int = 9) -> Iterable[Item]:
        since = dt.date.today() - dt.timedelta(days=days)
        stmt = (
            select(Item)
            .join(Stat)
            .where(Stat.date >= since)
            .order_by(Stat.views_total.desc())
            .limit(limit)
        )
        result = await self.session.scalars(stmt)
        return result.all()
