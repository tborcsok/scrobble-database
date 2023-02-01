import click
from tqdm import tqdm

from src import util
from src.dbschema import models
from src.lastfm import artists


@click.group("artist")
def artistgroup():
    util.raise_missing_db()


@artistgroup.command("tags")
@click.option(
    "--full",
    is_flag=True,
    help="Collect all artist tag info available at Last.fm, not just new artists",
)
def artisttag_collection(full: bool):

    artist_list = models.Scrobble.get_artist_list()

    if not full:
        artists_w_tag_info = models.ArtistTag.get_artist_list()
        artist_list = list(set(artist_list) - set(artists_w_tag_info))

    for artist in tqdm(artist_list):
        artist_id = models.Scrobble.get_artist_id(artist)

        artists.etl_artist_toptags(artist=artist, artist_id=artist_id)


@artistgroup.command("similar")
@click.option(
    "--full",
    is_flag=True,
    help="Collect all similar artist info available at Last.fm, not just new artists",
)
def similar_artist_collection(full: bool):

    artist_list = models.Scrobble.get_artist_list()

    if not full:
        artists_w_tag_info = models.ArtistSimilarity.get_artist_list()
        artist_list = list(set(artist_list) - set(artists_w_tag_info))

    for artist in tqdm(artist_list):
        artist_id = models.Scrobble.get_artist_id(artist)

        artists.etl_similar_artist(artist=artist, artist_id=artist_id)
