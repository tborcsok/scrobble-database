
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
    count int not null
);
