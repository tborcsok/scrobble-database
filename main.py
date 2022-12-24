import logging
import time
from datetime import datetime as dt
from typing import Optional

import click
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

from src import sql, utils
from src.lastfm import scrobbles


@click.command()
@click.option(
    "--full",
    is_flag=True,
    help="Collect all data available at Last.fm, do not stop data collection after reaching latest scrobble already written to DB",
)
def main(full: bool):

    last_timestamp: Optional[dt] = None
    if not full:
        last_timestamp = sql.sql_fetchone("select max(date) from dw.scrobbles")[0]
        logging.info("Most recent scrobble timestamp in db is %s", last_timestamp)
    else:
        logging.info("Loading all data from Last.fm")

    total_pages = scrobbles.get_total_pages()
    for p in tqdm(range(total_pages)):

        response = scrobbles.get_history(page=p + 1, from_ts=last_timestamp)
        records = scrobbles.extract_page(response)
        sql.insert_to_scrobbles(records)

        last_timestamp_page = dt.fromtimestamp(min(int(r.date) for r in records))
        if last_timestamp and last_timestamp_page < last_timestamp:
            logging.info("Loading data into database stopping with oldest scrobble at %s", last_timestamp_page)
            break


if __name__ == "__main__":

    utils.custom_logger()
    main()
