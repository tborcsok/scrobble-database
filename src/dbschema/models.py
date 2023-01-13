from datetime import datetime as dt
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Scrobble(Base):
    __tablename__ = "scrobble"
    # __table_args__ = {"schema": "track"}

    ts: Mapped[dt] = mapped_column(primary_key=True)
    artist: Mapped[Optional[str]] = mapped_column(String(512))
    album: Mapped[Optional[str]] = mapped_column(String(512))
    track: Mapped[Optional[str]] = mapped_column(String(512))
    artist_id: Mapped[Optional[str]] = mapped_column(String(64))
    album_id: Mapped[Optional[str]] = mapped_column(String(64))
    track_id: Mapped[Optional[str]] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"({self.ts}, {self.artist}, {self.album}, {self.track})"


class ArtistTag(Base):
    __tablename__ = "tag"
    # __table_args__ = {"schema": "artist"}

    artist: Mapped[str] = mapped_column(String(512), primary_key=True)
    artist_id: Mapped[Optional[str]] = mapped_column(String(64))
    tagname: Mapped[str] = mapped_column(String(256), primary_key=True)
    count: Mapped[int]

    def __repr__(self) -> str:
        return f"({self.artist}, {self.tagname}, {self.count})"


class ArtistSimilarity(Base):
    __tablename__ = "similar"
    # __table_args__ = {"schema": "artist"}

    artist: Mapped[str] = mapped_column(String(512), primary_key=True)
    artist_id: Mapped[Optional[str]] = mapped_column(String(64))
    similar_artist: Mapped[str] = mapped_column(String(512), primary_key=True)
    similar_artist_id: Mapped[Optional[str]] = mapped_column(String(64))
    similarity: Mapped[float]

    def __repr__(self) -> str:
        return f"({self.artist}, {self.similar_artist}, {self.similarity})"
