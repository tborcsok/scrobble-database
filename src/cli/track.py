import logging
from datetime import datetime as dt
from typing import Optional

import click
from tqdm import tqdm

from src import sql
from src.lastfm import scrobbles


@click.group("track")
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
