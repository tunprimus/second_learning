CREATE TABLE author (
	author_id INTEGER NOT NULL PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR
);

CREATE TABLE book (
	book_id INTEGER NOT NULL PRIMARY KEY,
	author_id INTEGER REFERENCES author,
	title VARCHAR
);

CREATE TABLE publisher (
	publisher_id INTEGER NOT NULL PRIMARY
	name VARCHAR
);
