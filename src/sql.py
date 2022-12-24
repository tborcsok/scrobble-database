from typing import Any, List, NamedTuple, Optional

import pandas as pd
import psycopg2
from psycopg2.extensions import connection

from src import schemas, setup


def connect_to_db() -> connection:

    conn = psycopg2.connect(dbname="postgres", user="postgres", password=setup.PG_PASSWORD, host="localhost")

    return conn


def sql_query(query: str) -> pd.DataFrame:
    """Return query result in a dataframe"""

    with connect_to_db() as conn:
        df = pd.read_sql(query, conn)

    return df


def sql_fetchone(query: str) -> Any:
    with connect_to_db() as conn:
        with conn.cursor() as c:
            c.execute(query)
            res = c.fetchone()
            return res


def sql_fetchall(query: str) -> Any:
    with connect_to_db() as conn:
        with conn.cursor() as c:
            c.execute(query)
            res = c.fetchall()
            return res


def insert_to_scrobbles(records=List[schemas.HistoryItem]):
    """Insert data to scrobbles table"""
    conn = connect_to_db()
    c = conn.cursor()
    c.executemany(
        (
            "insert into track.scrobble(date, artist, album, track, artist_id, album_id, track_id) "
            "values(to_timestamp(%s), %s, %s, %s, %s, %s, %s) "
            "on conflict on constraint scrobble_pkey do update set "
            "artist=EXCLUDED.artist, album=EXCLUDED.album, track=EXCLUDED.track, "
            "artist_id=EXCLUDED.artist_id, album_id=EXCLUDED.album_id, track_id=EXCLUDED.track_id "
        ),
        records,
    )
    conn.commit()

    c.close()
    conn.close()


def insert_to_artist_tags(artist: str, records=List[schemas.ArtistTagItem]):
    """Insert data to scrobbles table"""
    conn = connect_to_db()
    c = conn.cursor()

    c.execute("delete from artist.tag where artist=%s", (artist,))

    c.executemany(
        ("insert into artist.tag(artist, artist_id, tagname, count) values(%s, %s, %s, %s)"),
        records,
    )

    conn.commit()

    c.close()
    conn.close()
