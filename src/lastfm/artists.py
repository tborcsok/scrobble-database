from typing import List, Optional

import requests
from sqlalchemy import delete
from sqlalchemy.orm import Session

from src import exceptions
from src.dbschema import engine, models
from src.lastfm import base


def etl_artist_toptags(artist: str, artist_id: Optional[str] = None):

    resp = get_artist_toptags(artist=artist, artist_id=artist_id)
    records = extract_artist_toptags(artist=artist, artist_id=artist_id, resp=resp)

    if records:
        with Session(engine) as session:
            session.execute(delete(models.ArtistTag).where(models.ArtistTag.artist == artist))

            session.add_all(records)

            session.commit()


def get_artist_toptags(artist: str, artist_id: Optional[str] = None) -> requests.Response:
    params: base.RequestParams = {
        "method": "artist.gettoptags",
        "artist": artist,
    }
    if artist_id is not None:
        params["mbid"] = artist_id

    try:
        response = base.lastfm_get(params, cached=True)
    except exceptions.LastfmError:
        del params["mbid"]
        response = base.lastfm_get(params, cached=True)

    return response


def extract_artist_toptags(artist: str, artist_id: Optional[str], resp: requests.Response) -> List[models.ArtistTag]:

    tags = resp.json()["toptags"]["tag"]
    records = [models.ArtistTag(artist=artist, artist_id=artist_id, tagname=t["name"], count=t["count"]) for t in tags]

    return records


def etl_similar_artist(artist: str, artist_id: Optional[str] = None):

    resp = get_artist_similarartists(artist=artist, artist_id=artist_id)
    records = extract_artist_similarartists(artist=artist, artist_id=artist_id, resp=resp)

    if records:
        with Session(engine) as session:
            session.execute(delete(models.ArtistSimilarity).where(models.ArtistSimilarity.artist == artist))

            session.add_all(records)

            session.commit()


def get_artist_similarartists(artist: str, artist_id: Optional[str] = None) -> requests.Response:
    params: base.RequestParams = {
        "method": "artist.getsimilar",
        "artist": artist,
    }
    if artist_id is not None:
        params["mbid"] = artist_id

    try:
        response = base.lastfm_get(params, cached=True)
    except exceptions.LastfmError:
        del params["mbid"]
        response = base.lastfm_get(params, cached=True)

    return response


def extract_artist_similarartists(
    artist: str, artist_id: Optional[str], resp: requests.Response
) -> List[models.ArtistSimilarity]:

    similarartists = resp.json()["similarartists"]["artist"]

    records = []
    similar_artists = set()
    for r in similarartists:
        if (sim_artist_name := r["name"]) not in similar_artists:

            records.append(
                models.ArtistSimilarity(
                    artist=artist,
                    artist_id=artist_id,
                    similar_artist=sim_artist_name,
                    similar_artist_id=r.get("mbid"),
                    similarity=r["match"],
                )
            )

            similar_artists.add(sim_artist_name)

    return records
