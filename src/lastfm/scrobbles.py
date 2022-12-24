import logging
from datetime import datetime as dt
from typing import List, Optional

from requests import Response

from src import schemas, setup, sql
from src.lastfm import base

# scrobble


def get_total_pages() -> int:
    """Get number of total pages of scrobble history

    Parameters
    ----------
        from_ts: beginning timestamp of time range, UTC
    """
    response = get_scrobbles_page()
    totalpages = int(response.json()["recenttracks"]["@attr"]["totalPages"])
    logging.info("Total pages of scrobbles: %s", totalpages)
    return totalpages


def etl_scrobbles_page(page: int) -> dt:
    response = get_scrobbles_page(page=page)
    records = extract_scrobbles_page(response)
    sql.insert_to_scrobbles(records)

    last_timestamp_page = dt.fromtimestamp(min(int(r.date) for r in records))

    return last_timestamp_page


def get_scrobbles_page(page: Optional[int] = None) -> Response:
    """Get response from user.getRecentTracks service

    Params
    ----------
        page: page number to fetch
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

    response = base.lastfm_get(params)

    return response


def extract_scrobbles_page(response: Response) -> List[schemas.HistoryItem]:
    scrobbles = response.json()["recenttracks"]["track"]
    # skip 'Now Playing' track if it is included in response
    if (
        "@attr" in response.json()["recenttracks"]["track"][0].keys()
        and response.json()["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true"
    ):
        scrobbles = scrobbles[1:]

    records = []
    for s in scrobbles:
        records.append(
            schemas.HistoryItem(
                date=s["date"]["uts"],
                artist=s["artist"]["#text"],
                album=s["album"]["#text"],
                track=s["name"],
                artist_id=s["artist"]["mbid"],
                album_id=s["album"]["mbid"],
                track_id=s["mbid"],
            )
        )

    return records
