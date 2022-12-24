import logging
from datetime import datetime as dt
from typing import Optional

import click
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

from src import sql
from src.lastfm import artists, scrobbles


@click.group()
def cli():
    logging.basicConfig(
        format="%(levelname)s:%(asctime)s:%(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S%z",
    )


@cli.group("track")
def trackgroup():
    pass


@trackgroup.command("scrobbles")
@click.option(
    "--full",
    is_flag=True,
    help="Collect all scrobbles available at Last.fm, do not stop data collection after reaching latest scrobble already written to DB",
)
def scrobble_collection(full: bool):

    last_timestamp: Optional[dt] = None
    if not full:
        last_timestamp = sql.sql_fetchone("select max(date) from track.scrobble")[0]
        logging.info("Most recent scrobble timestamp in db is %s", last_timestamp)
    else:
        logging.info("Loading all data from Last.fm")

    total_pages = scrobbles.get_total_pages()
    for p in tqdm(range(total_pages)):

        last_timestamp_page = scrobbles.etl_scrobbles_page(p + 1)

        if last_timestamp and last_timestamp_page < last_timestamp:
            logging.info("Sync with database finished, oldest inserted scrobble at %s", last_timestamp_page)
            break


@cli.group("artist")
def artistgroup():
    pass


@artistgroup.command("tags")
def artisttag_collection():
    unique_artists = sql.sql_fetchall(
        (
            "select d.artist, d.artist_id from ( "
            "	select distinct on (artist) artist, artist_id from track.scrobble "
            ") d join ( "
            "	select artist, count(*) as play_count from track.scrobble "
            "	where artist is not null "
            "	group by artist "
            ") n using (artist) "
            "order by n.play_count desc "
        )
    )

    for artist, artist_id in tqdm(unique_artists):
        artists.etl_artist_toptags(artist=artist, artist_id=artist_id)


if __name__ == "__main__":

    cli()
