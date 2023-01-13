import logging

from src import dbschema
from src.dbschema import models


def init_database():
    """Initialize database"""

    logging.info("Initializing database")

    models.Base.metadata.create_all(dbschema.engine)
