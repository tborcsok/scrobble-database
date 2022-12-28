from typing import List, Optional

import requests

from src import exceptions, schemas, sql
from src.lastfm import base


def etl_artist_toptags(artist: str, artist_id: Optional[str] = None):

    resp = get_artist_toptags(artist=artist, artist_id=artist_id)
    records = extract_artist_toptags(artist=artist, artist_id=artist_id, resp=resp)
    sql.insert_to_artist_tags(artist=artist, records=records)


def get_artist_toptags(artist: str, artist_id: Optional[str] = None) -> requests.Response:
    params: base.RequestParams = {
        "method": "artist.gettoptags",
        "artist": artist,
    }
    if artist_id is not None:
        params["mbid"] = artist_id

    try:
        response = base.lastfm_get_w_caching(params)
    except exceptions.LastfmError:
        del params["mbid"]
        response = base.lastfm_get_w_caching(params)

    return response


def extract_artist_toptags(
    artist: str, artist_id: Optional[str], resp: requests.Response
) -> List[schemas.ArtistTagItem]:

    tags = resp.json()["toptags"]["tag"]
    records = [
        schemas.ArtistTagItem(artist=artist, artist_id=artist_id, tagname=t["name"], count=t["count"]) for t in tags
    ]

    return records


def etl_similar_artist(artist: str, artist_id: Optional[str] = None):

    resp = get_artist_similarartists(artist=artist, artist_id=artist_id)
    records = extract_artist_similarartists(artist=artist, artist_id=artist_id, resp=resp)
    sql.insert_to_similar_artist(artist=artist, records=records)


def get_artist_similarartists(artist: str, artist_id: Optional[str] = None) -> requests.Response:
    params: base.RequestParams = {
        "method": "artist.getsimilar",
        "artist": artist,
    }
    if artist_id is not None:
        params["mbid"] = artist_id

    try:
        response = base.lastfm_get_w_caching(params)
    except exceptions.LastfmError:
        del params["mbid"]
        response = base.lastfm_get_w_caching(params)

    return response


def extract_artist_similarartists(
    artist: str, artist_id: Optional[str], resp: requests.Response
) -> List[schemas.SimilarArtistItem]:

    similarartists = resp.json()["similarartists"]["artist"]

    records = [
        schemas.SimilarArtistItem(
            artist=artist,
            artist_id=artist_id,
            similar_artist=r["name"],
            similar_artist_id=r.get("mbid"),
            similarity=r["match"],
        )
        for r in similarartists
    ]

    return records
