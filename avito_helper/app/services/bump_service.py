from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from ..core.avito_client import AvitoClient
from .stats_service import StatsService


class BumpService:
    def __init__(self, client: AvitoClient, session: AsyncSession) -> None:
        self.client = client
        self.session = session
        self.stats_service = StatsService(client, session)

    async def bump_top9(self) -> None:
        top_items = await self.stats_service.top_items()
        for item in top_items:
            self.client.post(f"/items/{item.id}/bump")
