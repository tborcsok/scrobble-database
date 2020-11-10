import time
import datetime
import logging

from tqdm import tqdm

from src.lastfm import scrobbles
from src import sql
from src import utils

def main():

    last_timestamp = sql.get_last_scrobble_datetime()

    total_pages = scrobbles.get_total_pages()
    try_again=list()
    for p in tqdm(range(total_pages)):
        try:
            response = scrobbles.get_history(page=p+1)
            df = scrobbles.extract_page(response)
            sql.insert_to_sqlite(df)
            if datetime.datetime.strptime(df.date.min(), "%Y-%m-%d %H:%M:%S") < last_timestamp:
                logging.info("no new data")
                break
            else:
                time.sleep(0.5)
        except KeyboardInterrupt:
            break
        except:
            try_again.append(p+1)

if __name__ == '__main__':
    utils.custom_logger()
    main()
        
