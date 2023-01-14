from src.setup import DB_PATH


def check_db_exists() -> bool:
    """Check if database file exists"""

    return DB_PATH.exists()


def raise_missing_db() -> None:
    """Raise error if database file does not exist

    Raises:
        FileNotFoundError if file does not exist
    """
    if not DB_PATH.exists():
        raise FileNotFoundError('Database file not found. Run the "db init" command first to initialize the database!')
