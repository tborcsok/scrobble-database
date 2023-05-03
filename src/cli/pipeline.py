import logging
from enum import Enum

import click

from src import util
from src.cli.artist import artisttag_collection, similar_artist_collection
from src.cli.track import scrobble_collection


class PipelineSettings(Enum):
    SYNC = (False, "syncing")
    INIT = (True, "initializing")

    def __init__(self, full, actionverb) -> None:
        self.full: bool = full
        self.actionverb: str = actionverb


@click.group("pipeline")
def pipelinegroup():
    """Data collection pipeline that collects all data types"""
    util.raise_missing_db()


@pipelinegroup.command("sync")
@click.pass_context
def sync(ctx: click.Context):
    pipeline(PipelineSettings.SYNC, ctx)


@pipelinegroup.command("init")
@click.pass_context
def init(ctx: click.Context):
    pipeline(PipelineSettings.INIT, ctx)


def pipeline(mode: PipelineSettings, context: click.Context):
    logging.info("%s scrobbles", mode.actionverb)
    context.invoke(scrobble_collection, full=mode.full)

    logging.info("%s artist tags", mode.actionverb)
    context.invoke(artisttag_collection, full=mode.full)

    logging.info("%s similar artists", mode.actionverb)
    context.invoke(similar_artist_collection, full=mode.full)
