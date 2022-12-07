
CREATE TABLE scrobbles (
    date timestamp without time zone not null,
    artist varchar(64) not null,
    album varchar(64) not null,
    track varchar(64) not null,
    artist_id varchar(64) null,
    album_id varchar(64) null,
    track_id varchar(64) null
);
