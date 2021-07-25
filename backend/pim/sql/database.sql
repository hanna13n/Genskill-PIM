drop table if exists notes cascade;
drop table if exists hashtags cascade;
drop table if exists tags_notes cascade;

create table hashtags(
    id serial primary key,
    tagname text UNIQUE NOT NULL
);
insert into hashtags(tagname) values('important'),('starred');

create table notes(
    id serial primary key,
    title text NOT NULL,
    created_on timestamp,
    detail text
);

create table tags_notes(
    note serial references notes(id),
    tag serial references hashtags(id)
);