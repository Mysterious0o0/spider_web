create database STAR_TABLE charset=utf8;
use STAR_TABLE;
create table star_photos(id varchar(64) primary key not null, star varchar(64),release_time date,star_img_path varchar(128),star_url varchar(128),star_update_time datetime);
