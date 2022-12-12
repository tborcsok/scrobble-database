
create schema dw;

create table dw.scrobbles (
    date timestamp without time zone not null primary key,
    artist varchar(512) null,
    album varchar(512) null,
    track varchar(512) null,
    artist_id varchar(64) null,
    album_id varchar(64) null,
    track_id varchar(64) null
);
