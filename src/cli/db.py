from pathlib import Path

import click

from src.dbschema import initialize


@click.group()
def db():
    pass


@db.command()
def init():

    initialize.init_database()


@db.command()
def recreate():
    Path("lastfm.db").unlink(missing_ok=True)

    initialize.init_database()
