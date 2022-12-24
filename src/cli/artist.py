import click
from tqdm import tqdm

from src import sql
from src.lastfm import artists


@click.group("artist")
def artistgroup():
    pass


@artistgroup.command("tags")
@click.option(
    "--full",
    is_flag=True,
    help="Collect all artist info available at Last.fm, not just new artists",
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
