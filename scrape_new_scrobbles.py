import time
import logging

from tqdm import tqdm

from src.lastfm import scrobbles
from src import sql
from src import utils


def main():

    last_timestamp = sql.get_last_scrobble_datetime()

    total_pages = scrobbles.get_total_pages(from_ts=last_timestamp)
    errors = list()
    for p in tqdm(range(total_pages)):
        try:
            response = scrobbles.get_history(page=p + 1, from_ts=last_timestamp)
            df = scrobbles.extract_page(response)
            sql.insert_to_sqlite(df, "scrobbles")
        except KeyboardInterrupt:
            break
        except:
            logging.error("Error", exc_info=True)
            errors.append(p + 1)
        finally:
            time.sleep(0.5)
   
    print(errors)


if __name__ == "__main__":
    utils.custom_logger()
    main()
