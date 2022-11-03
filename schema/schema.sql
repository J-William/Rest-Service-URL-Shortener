create schema url_shortener;

create table url_shortener.mapping(
	mapkey varchar PRIMARY KEY,
	url varchar UNIQUE	
);
