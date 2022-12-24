import logging
from dataclasses import dataclass
from datetime import datetime as dt
from typing import List, NamedTuple, Optional

import pandas as pd
from requests import Response

from src import setup, utils
from src.lastfm import base

# scrobble


class HistoryItem(NamedTuple):
    date: str
    artist: str
    album: str
    track: str
    artist_id: Optional[str]
    album_id: Optional[str]
    track_id: Optional[str]


def get_history(page: Optional[int] = None, from_ts: Optional[dt] = None) -> Response:
    """Get response from user.getRecentTracks service

    Params
    ----------
        page: page number to fetch
        from_ts: beginning timestamp of time range, UTC
    """
    params: base.RequestParams = {
        "method": "user.getRecentTracks",
        "user": setup.LASTFM_API_USER,
        "limit": 200,
        "extended": 0,
        "to": dt.now().timestamp(),
    }
    if page is not None:
        params["page"] = page
    if from_ts is not None:
        params["from"] = utils.dt2ts(from_ts, addone=True)

    response = base.lastfm_get(params)

    return response


def get_total_pages(from_ts: Optional[dt] = None):
    """Get number of total pages of scrobble history

    Parameters
    ----------
        from_ts: beginning timestamp of time range, UTC
    """
    response = get_history(from_ts=from_ts)
    totalpages = int(response.json()["recenttracks"]["@attr"]["totalPages"])
    logging.info("Total pages of scrobbles: %s", totalpages)
    return totalpages


json_extract = {
    "date": ["date", "uts"],
    "artist": ["artist", "#text"],
    "album": ["album", "#text"],
    "track": ["name"],
    "artist_id": ["artist", "mbid"],
    "album_id": ["album", "mbid"],
    "track_id": ["mbid"],
}


def extract_page(response: Response) -> List[HistoryItem]:
    scrobbles = response.json()["recenttracks"]["track"]
    # skip 'Now Playing' track if it is included in response
    if (
        "@attr" in response.json()["recenttracks"]["track"][0].keys()
        and response.json()["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true"
    ):
        scrobbles = scrobbles[1:]

    records = list()
    for s in scrobbles:
        records.append(HistoryItem(*[utils.recurGet(s, i) for i in json_extract.values()]))

    return records
