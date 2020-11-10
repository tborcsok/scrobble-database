import datetime

import pandas as pd

from src import setup
from src.lastfm import base
from src import utils

# scrobble

def get_history(page=None):
    params = {
        "method": "user.getRecentTracks",
        "user": setup.LASTFM_API_USER,
        "limit": 200,
        "extended": 0
    }
    if page is not None:
        params["page"] = page

    response = base.lastfm_get(params)
    return response

def get_total_pages():
    response = get_history()
    return int(response.json()['recenttracks']['@attr']['totalPages'])

json_extract = {
    "date": ["date", "uts"],
    "artist": ["artist", "#text"],
    "album": ["album", "#text"],
    "track": ["name"],
    "artist_id": ["artist", "mbid"],
    "album_id": ["album", "mbid"],
    "track_id": ["mbid"],
}

def extract_page(response):
    scrobbles = response.json()["recenttracks"]["track"]
    # skip 'Now Playing' track if it is included in response
    if '@attr' in response.json()["recenttracks"]["track"][0].keys() and \
        response.json()["recenttracks"]["track"][0]['@attr']['nowplaying']=='true':
        scrobbles = scrobbles[1:]
    
    records = list()
    for s in scrobbles:
        records.append([utils.recurGet(s, i) for i in json_extract.values()])
        
    df = pd.DataFrame(records, 
                      columns=json_extract.keys())
    df["date"] = df["date"].apply(lambda x: datetime.datetime.utcfromtimestamp(int(x)).strftime("%Y-%m-%d %H:%M:%S"))

    return df

