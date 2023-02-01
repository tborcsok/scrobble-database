import click

from src.dbschema import initialize
from src.util import DB_PATH


@click.group()
def db():
    pass


@db.command()
def init():

    initialize.init_database()


@db.command()
def recreate():
    DB_PATH.unlink(missing_ok=True)

    initialize.init_database()
