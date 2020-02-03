-- we don't know how to generate schema main (class Schema) :(
drop table skills_vacancies;
drop table regions;
drop table skills;
drop table vacancies;

create table regions
(
	city varchar(50),
	country varchar(20),
	region varchar(100),
	created datetime,
	id integer
		constraint regions_pk
			primary key autoincrement
);

create unique index regions_city_country_region_uindex
	on regions (city, country, region);

create unique index regions_id_uindex
	on regions (id);

create table skills
(
	id integer
		primary key autoincrement,
	created datetime,
	name varchar(150) not null
		unique
		on conflict ignore
);

create table vacancies
(
	id integer not null
		unique
		on conflict ignore,
	name varchar(200),
	url varchar(300),
	file_name varchar(200),
	min_salary numeric,
	max_salary numeric,
	created datetime,
	updated datetime,
	region_id integer not null
		references regions,
	experience integer not null
);

create table skills_vacancies
(
	vacancy_id integer not null
		references vacancies (id),
	skills_id integer
		references skills(id)
);

