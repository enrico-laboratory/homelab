from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy.orm import Mapped


class Base(DeclarativeBase):
    pass


class ChoirTable(Base):
    __tablename__ = 'choir'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(30), unique=True)

    def __repr__(self) -> str:
        return f"ChoirTable(id={self.id!r}, id_notion={self.id_notion!r}, name={self.name!r})"


class LocationTable(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(30))
    address: Mapped[Optional[str]] = mapped_column(String())
    purpose: Mapped[Optional[str]] = mapped_column(String())

    def __repr__(self) -> str:
        return f"LocationTable(id={self.id!r}, name={self.name!r}, city={self.city!r})"


class MusicProjectTable(Base):
    __tablename__ = 'music_project'

    id: Mapped[int] = mapped_column(primary_key=True)
    choir_id: Mapped[Optional[int]] = mapped_column(ForeignKey("choir.id"))
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(30))
    year: Mapped[int] = mapped_column(Integer())
    status: Mapped[Optional[str]] = mapped_column(String(30))
    excerpt: Mapped[Optional[str]] = mapped_column(String())
    description: Mapped[Optional[str]] = mapped_column(String())

    choir = relationship("ChoirTable", foreign_keys=[choir_id])

    def __repr__(self) -> str:
        return f"MusicProjectTable(id={self.id!r}, name={self.name!r}, year={self.year!r}, choir_id={self.choir_id!r})"


class TaskTable(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_notion: Mapped[Optional[str]] = mapped_column(String(36))
    name: Mapped[Optional[str]] = mapped_column(String(30))
    start_date_time: Mapped[datetime] = mapped_column(DateTime())
    end_date_time: Mapped[Optional[datetime]] = mapped_column(DateTime())
    type: Mapped[Optional[str]] = mapped_column(String(15))
    music_project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("music_project.id"))
    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("locations.id"))

    music_project = relationship(
        "MusicProjectTable", foreign_keys=[music_project_id])
    location = relationship(
        "LocationTable", foreign_keys=[location_id])
    
    def __repr__(self) -> str:
        return f"TaskTable(id={self.id!r}, name={self.name!r}, start_date_time={self.start_date_time!r}, end_date_time={self.end_date_time!r}, type={self.type!r}, music_project_id={self.music_project_id!r})"
