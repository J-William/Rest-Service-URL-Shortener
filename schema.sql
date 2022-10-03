create schema url_shortener;

create table url_shortener.mapping(
	original_url varchar,
	mapkey varchar
);
