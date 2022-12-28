from typing import NamedTuple, Optional


class HistoryItem(NamedTuple):
    date: str
    artist: str
    album: str
    track: str
    artist_id: Optional[str]
    album_id: Optional[str]
    track_id: Optional[str]


class ArtistTagItem(NamedTuple):
    artist: str
    artist_id: Optional[str]
    tagname: str
    count: int


class SimilarArtistItem(NamedTuple):
    artist: str
    artist_id: Optional[str]
    similar_artist: str
    similar_artist_id: Optional[str]
    similarity: float
