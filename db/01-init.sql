
create schema track;

create table track.scrobble (
    date timestamp without time zone not null primary key,
    artist varchar(512) null,
    album varchar(512) null,
    track varchar(512) null,
    artist_id varchar(64) null,
    album_id varchar(64) null,
    track_id varchar(64) null
);

create schema artist;

create table artist.tag (
    artist varchar(512) not null,
    artist_id varchar(64) null,
    tagname varchar(256) not null,
    count int not null,
    constraint unique_artisttag primary key (artist, tagname)
);

create table artist.similar (
    artist varchar(512) not null,
    artist_id varchar(64) null,
    similar_artist varchar(512) not null,
    similar_artist_id varchar(64) null,
    similarity real,
    constraint unique_similarartist primary key (artist, similar_artist)
);
