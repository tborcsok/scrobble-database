import datetime

import pytz

from src import utils
from src.lastfm import base

# scrobble


def get_artist_info(mbid):
    params = {"method": "artist.getInfo", "mbid": mbid}

    response = base.lastfm_get(params)
    now = datetime.datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
    return response, now


json_extract = {
    "listeners": ["stats", "listeners"],
    "playcount": ["stats", "playcount"],
}


def extract_artist(response, a, download_time):
    if "error" in response.json().keys():
        empty_stats = [None for i in json_extract.keys()]
        return [a] + empty_stats + [download_time]
    else:
        artist = response.json()["artist"]

        stats = [utils.recurGet(artist, i) for i in json_extract.values()]

        return [a] + stats + [download_time]
