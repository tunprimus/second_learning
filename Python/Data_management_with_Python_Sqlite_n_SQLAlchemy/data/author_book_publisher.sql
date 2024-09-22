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

SELECT * FROM author;

INSERT INTO author
	(first_name, last_name)
VALUES ("Paul", "Mendez");

UPDATE author
SET first_name = "Richard", last_name = "Bachman"
WHERE first_name = "Stephen" AND last_name = "King";

DELETE FROM author
WHERE first_name = "Paul"
AND last_name = "Mendez";

SELECT
  *
FROM some_table
WHERE active = 1;

SELECT
a.first_name || ' ' || a.last_name AS author_name,
b.title AS book_title
FROM author a
JOIN book b ON b.author_id = a.author_id
ORDER BY a.last_name ASC;


CREATE TABLE author_publisher (
    author_id INTEGER REFERENCES author,
    publisher_id INTEGER REFERENCES publisher
);

SELECT
a.first_name || ' ' || a.last_name AS author_name,
p.name AS publisher_name
FROM author a
JOIN author_publisher ap ON ap.author_id = a.author_id
JOIN publisher p ON p.publisher_id = ap.publisher_id
ORDER BY a.last_name ASC;

SELECT
a.first_name || ' ' || a.last_name AS author_name,
COUNT(b.title) AS total_books
FROM author a
JOIN book b ON b.author_id = a.author_id
GROUP BY author_name
ORDER BY total_books DESC, a.last_name ASC;
