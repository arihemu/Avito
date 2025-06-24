from __future__ import annotations

import datetime as dt
from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession

from ..core.avito_client import AvitoClient


class ChatService:
    def __init__(self, client: AvitoClient, session: AsyncSession) -> None:
        self.client = client
        self.session = session

    def collect_messages(self) -> dict[str, dict[int, int]]:
        resp = self.client.get("/messenger/messages")
        messages = resp.json().get("messages", [])
        heat_map: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))
        for msg in messages:
            created = dt.datetime.fromisoformat(msg["created_at"]).astimezone()
            day = created.strftime("%Y-%m-%d")
            hour = created.hour
            heat_map[day][hour] += 1
        return heat_map
