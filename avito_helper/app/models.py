from __future__ import annotations

import datetime as dt

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)

    stats: Mapped[list[Stat]] = relationship("Stat", back_populates="item")
    descriptions: Mapped[list[DescriptionSnapshot]] = relationship(
        "DescriptionSnapshot", back_populates="item"
    )


class Stat(Base):
    __tablename__ = "stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    date: Mapped[dt.date] = mapped_column(Date)
    views_total: Mapped[int] = mapped_column(Integer)

    item: Mapped[Item] = relationship("Item", back_populates="stats")


class DescriptionSnapshot(Base):
    __tablename__ = "description_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, default=dt.datetime.utcnow
    )
    description_hash: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String)

    item: Mapped[Item] = relationship("Item", back_populates="descriptions")
