import click

from src.cli import artist, db, pipeline, track


@click.group()
def cli():
    pass


cli.add_command(artist.artistgroup)

cli.add_command(track.trackgroup)

cli.add_command(pipeline.pipelinegroup)

cli.add_command(db.db)
