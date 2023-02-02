import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]

LASTFM_API_USER = os.environ["LASTFM_API_USER"]
LASTFM_API_KEY = os.environ["LASTFM_API_KEY"]

DB_PATH = PROJECT_ROOT / "lastfm.db"
