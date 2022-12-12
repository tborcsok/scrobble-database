from typing import List

import pandas as pd
import psycopg2
from psycopg2.extensions import connection

from src import setup
from src.lastfm import scrobbles


def connect_to_db() -> connection:

    conn = psycopg2.connect(dbname="postgres", user="postgres", password=setup.PG_PASSWORD, host="localhost")

    return conn


def sql_query(query: str) -> pd.DataFrame:
    """Return query result in a dataframe"""

    with connect_to_db() as conn:
        df = pd.read_sql(query, conn)

    return df


def insert_to_scrobbles(records=List[scrobbles.HistoryItem]):
    """Insert data to scrobbles table"""
    conn = connect_to_db()
    c = conn.cursor()
    c.executemany(
        (
            "insert into dw.scrobbles(date, artist, album, track, artist_id, album_id, track_id) "
            "values(to_timestamp(%s), %s, %s, %s, %s, %s, %s) "
            "on conflict on constraint scrobbles_pkey do update set "
            "artist=EXCLUDED.artist, album=EXCLUDED.album, track=EXCLUDED.track, "
            "artist_id=EXCLUDED.artist_id, album_id=EXCLUDED.album_id, track_id=EXCLUDED.track_id "
        ),
        records,
    )
    conn.commit()

    c.close()
    conn.close()
