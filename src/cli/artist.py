import click
from tqdm import tqdm

from src import sql, util
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
    if full:
        unique_artists = sql.sql_fetchall(
            (
                "select d.artist, d.artist_id from ( "
                "	select distinct on (artist) artist, artist_id from track.scrobble "
                ") d join ( "
                "	select artist, count(*) as play_count from track.scrobble "
                "	where artist is not null "
                "	group by artist "
                ") n using (artist) "
                "order by n.play_count desc "
            )
        )
    else:
        unique_artists = sql.sql_fetchall(
            (
                "select d.artist, d.artist_id from ( "
                "	select distinct on (artist) artist, artist_id from track.scrobble "
                ") d left join artist.tag t on d.artist = t.artist where t.artist is null "
            )
        )

    for artist, artist_id in tqdm(unique_artists):
        artists.etl_artist_toptags(artist=artist, artist_id=artist_id)


@artistgroup.command("similar")
@click.option(
    "--full",
    is_flag=True,
    help="Collect all similar artist info available at Last.fm, not just new artists",
)
def similar_artist_collection(full: bool):
    if full:
        unique_artists = sql.sql_fetchall(
            (
                "select d.artist, d.artist_id from ( "
                "	select distinct on (artist) artist, artist_id from track.scrobble "
                ") d join ( "
                "	select artist, count(*) as play_count from track.scrobble "
                "	where artist is not null "
                "	group by artist "
                ") n using (artist) "
                "order by n.play_count desc "
            )
        )
    else:
        unique_artists = sql.sql_fetchall(
            (
                "select d.artist, d.artist_id from ( "
                "	select distinct on (artist) artist, artist_id from track.scrobble "
                ") d left join artist.similar s on d.artist = s.artist where s.artist is null "
            )
        )

    for artist, artist_id in tqdm(unique_artists):
        artists.etl_similar_artist(artist=artist, artist_id=artist_id)
