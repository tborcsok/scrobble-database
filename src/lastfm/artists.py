import datetime
import logging

import pytz

from src.lastfm import base
from src import utils

# scrobble

def get_artist(mbid):
    params = {
        "method": "artist.getInfo",
        "mbid": mbid
    }

    response = base.lastfm_get(params)
    now = datetime.datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
    return response, now

json_extract = {
    "listeners": ["stats", "listeners"],
    "playcount": ["stats", "playcount"]
}

def extract_artist(response):
    if "error" in response.json().keys():
        return [None for i in json_extract.keys()]
    else:
        artist = response.json()["artist"]

        stats = [utils.recurGet(artist, i) for i in json_extract.values()]

        return stats

