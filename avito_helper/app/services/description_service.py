from __future__ import annotations

import hashlib
import json
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.avito_client import AvitoClient
from ..models import DescriptionSnapshot, Item


class DescriptionService:
    def __init__(self, client: AvitoClient, session: AsyncSession) -> None:
        self.client = client
        self.session = session

    async def monitor_competitors(self, competitor_ids: Iterable[int]) -> None:
        for item_id in competitor_ids:
            resp = self.client.get(f"/items/{item_id}")
            data = resp.json()
            description = data.get("description", "")
            hsh = hashlib.sha256(description.encode()).hexdigest()

            stmt = (
                select(DescriptionSnapshot)
                .where(DescriptionSnapshot.item_id == item_id)
                .order_by(DescriptionSnapshot.created_at.desc())
            )
            result = await self.session.scalars(stmt)
            last_snapshot = result.first()
            if not last_snapshot or last_snapshot.description_hash != hsh:
                snapshot = DescriptionSnapshot(
                    item_id=item_id,
                    description_hash=hsh,
                    description=description,
                )
                self.session.add(snapshot)
        await self.session.commit()
