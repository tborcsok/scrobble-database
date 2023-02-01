from datetime import datetime as dt
from typing import List, Optional

from sqlalchemy import String, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from src.dbschema import engine


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

    @classmethod
    def get_last_timestamp(cls) -> Optional[dt]:

        stmt = select(func.max(cls.ts))

        with Session(engine) as session:
            last_timestamp: Optional[dt] = session.scalars(stmt).first()

        return last_timestamp

    @classmethod
    def get_artist_list(cls) -> List[str]:

        stmt = select(cls.artist).group_by(cls.artist).order_by(func.count().desc())

        with Session(engine) as session:
            artist_list: List[str] = session.scalars(stmt).all()

        return artist_list

    @classmethod
    def get_artist_id(cls, artist: str) -> Optional[str]:

        stmt = select(cls.artist_id).where(cls.artist == artist).order_by(cls.artist_id.desc())

        with Session(engine) as session:
            artist_id: Optional[str] = session.scalars(stmt).first()

        return artist_id


class ArtistTag(Base):
    __tablename__ = "tag"
    # __table_args__ = {"schema": "artist"}

    artist: Mapped[str] = mapped_column(String(512), primary_key=True)
    artist_id: Mapped[Optional[str]] = mapped_column(String(64))
    tagname: Mapped[str] = mapped_column(String(256), primary_key=True)
    count: Mapped[int]

    def __repr__(self) -> str:
        return f"({self.artist}, {self.tagname}, {self.count})"

    @classmethod
    def get_artist_list(cls) -> List[str]:

        stmt = select(cls.artist).group_by(cls.artist)

        with Session(engine) as session:
            artist_list: List[str] = session.scalars(stmt).all()

        return artist_list


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

    @classmethod
    def get_artist_list(cls) -> List[str]:

        stmt = select(cls.artist).group_by(cls.artist)

        with Session(engine) as session:
            artist_list: List[str] = session.scalars(stmt).all()

        return artist_list
