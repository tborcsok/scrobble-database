import os
from pathlib import Path

LASTFM_API_USER = os.environ["LASTFM_API_USER"]
LASTFM_API_KEY = os.environ["LASTFM_API_KEY"]

DB_FILE = "lastfm.db"
DB_PATH = Path(DB_FILE)
