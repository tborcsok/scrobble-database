import click

from src.cli import artist, track


@click.group()
def cli():
    pass


cli.add_command(artist.artistgroup)

cli.add_command(track.trackgroup)
