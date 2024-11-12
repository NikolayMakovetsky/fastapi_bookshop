SET search_path TO users,public;
DROP SCHEMA IF EXISTS users CASCADE;
CREATE SCHEMA users;

CREATE TABLE "user"
(
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	username varchar(30) NOT NULL,
	email varchar(320) NOT NULL,
	hashed_password varchar(1024) NOT NULL,
	is_active boolean NOT NULL,
	is_superuser boolean NOT NULL,
	is_verified boolean NOT NULL,
	user_created integer NOT NULL,
	date_created varchar(50) NOT NULL,
	user_modified integer,
	date_modified varchar(50),
	row_version integer NOT NULL
);
CREATE UNIQUE INDEX user_email_index ON "user" (email);



/*
SELECT * FROM users."user";

SELECT * FROM author;
SELECT * FROM genre;
SELECT * FROM book;
SELECT * FROM city;
SELECT * FROM client;
SELECT * FROM step;
SELECT * FROM buy;
SELECT * FROM buy_step;
SELECT * FROM buy_book;

SELECT a.*, b.name_author, c.name_genre FROM book a
JOIN author b ON b.author_id = a.author_id
JOIN genre c ON c.genre_id = a.genre_id;
*/



SET search_path TO books,public;
DROP SCHEMA IF EXISTS books CASCADE;
CREATE SCHEMA books;


CREATE TABLE author
(
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name_author varchar(30) NOT NULL,
	user_created integer NOT NULL,
	date_created varchar(50) NOT NULL,
	user_modified integer,
	date_modified varchar(50),
	row_version integer NOT NULL
);

CREATE TABLE genre
(
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name_genre varchar(30) NOT NULL,
	user_created integer NOT NULL,
	date_created varchar(50) NOT NULL,
	user_modified integer,
	date_modified varchar(50),
	row_version integer NOT NULL
);

CREATE TABLE book
(
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	title varchar(50) NOT NULL,
	author_id integer NOT NULL,
	genre_id integer NOT NULL,
	price decimal(10,2) NOT NULL,
	amount integer NOT NULL,
	user_created integer NOT NULL,
	date_created varchar(50) NOT NULL,
	user_modified integer,
	date_modified varchar(50),
	row_version integer NOT NULL
);
ALTER TABLE book ADD FOREIGN KEY (author_id) REFERENCES author (id);
ALTER TABLE book ADD FOREIGN KEY (genre_id) REFERENCES genre (id);

CREATE TABLE city
(
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name_city varchar(30) NOT NULL,
	days_delivery integer NOT NULL,
	user_created integer NOT NULL,
	date_created varchar(50) NOT NULL,
	user_modified integer,
	date_modified varchar(50),
	row_version integer NOT NULL
);

CREATE TABLE client
(
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name_client varchar(50) NOT NULL,
	city_id integer NOT NULL,
	email varchar(30) NOT NULL,
	user_created integer NOT NULL,
	date_created varchar(50) NOT NULL,
	user_modified integer,
	date_modified varchar(50),
	row_version integer NOT NULL
);
ALTER TABLE client ADD FOREIGN KEY (city_id) REFERENCES city (id);

CREATE TABLE buy
(
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	buy_description varchar(100) NULL,
	client_id integer NOT NULL,
	user_created integer NOT NULL,
	date_created varchar(50) NOT NULL,
	user_modified integer,
	date_modified varchar(50),
	row_version integer NOT NULL
);
ALTER TABLE buy ADD FOREIGN KEY (client_id) REFERENCES client (id);

CREATE TABLE step
(
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name_step varchar(30) NOT NULL,
	user_created integer NOT NULL,
	date_created varchar(50) NOT NULL,
	user_modified integer,
	date_modified varchar(50),
	row_version integer NOT NULL
);

CREATE TABLE buy_book
(
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	buy_id integer NOT NULL,
	book_id integer NOT NULL,
	amount integer NOT NULL,
	user_created integer NOT NULL,
	date_created varchar(50) NOT NULL,
	user_modified integer,
	date_modified varchar(50),
	row_version integer NOT NULL
);
ALTER TABLE buy_book ADD FOREIGN KEY (buy_id) REFERENCES buy (id);
ALTER TABLE buy_book ADD FOREIGN KEY (book_id) REFERENCES book (id);

CREATE TABLE buy_step
(
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	buy_id integer NOT NULL,
	step_id integer NOT NULL,
	date_step_beg DATE,
	date_step_end DATE,
	user_created integer NOT NULL,
	date_created varchar(50) NOT NULL,
	user_modified integer,
	date_modified varchar(50),
	row_version integer NOT NULL
);
ALTER TABLE buy_step ADD FOREIGN KEY (buy_id) REFERENCES buy (id);
ALTER TABLE buy_step ADD FOREIGN KEY (step_id) REFERENCES step (id);

INSERT INTO author (name_author, user_created, date_created, user_modified, date_modified, row_version)
VALUES ('Булгаков М.А.', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Достоевский Ф.М.', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Есенин С.А.', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Пастернак Б.Л.', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Лермонтов М.Ю.', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0);

INSERT INTO genre (name_genre, user_created, date_created, user_modified, date_modified, row_version)
VALUES ('Роман', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Поэзия', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Приключения', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0);

INSERT INTO book (title, author_id, genre_id, price, amount, user_created, date_created, user_modified, date_modified, row_version)
VALUES  ('Мастер и Маргарита', 1, 1, 670.99, 3, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
        ('Белая гвардия ', 1, 1, 540.50, 5, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
        ('Идиот', 2, 1, 460.00, 10, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
        ('Братья Карамазовы', 2, 1, 799.01, 2, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
        ('Игрок', 2, 1, 480.50, 10, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
        ('Стихотворения и поэмы', 3, 2, 650.00, 15, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
        ('Черный человек', 3, 2, 570.20, 6, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
        ('Лирика', 4, 2, 518.99, 2, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0);

INSERT INTO city (name_city, days_delivery, user_created, date_created, user_modified, date_modified, row_version)
VALUES ('Москва', 5, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Санкт-Петербург', 3, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Владивосток', 12, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0);

INSERT INTO client (name_client, city_id, email, user_created, date_created, user_modified, date_modified, row_version)
VALUES ('Баранов Павел', 3, 'baranov@test', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Абрамова Катя', 1, 'abramova@test', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Семенонов Иван', 2, 'semenov@test', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Яковлева Галина', 1, 'yakovleva@test', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0);

INSERT INTO buy (buy_description, client_id, user_created, date_created, user_modified, date_modified, row_version)
VALUES ('Доставка только вечером', 1, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (NULL, 3, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Упаковать каждую книгу по отдельности', 2, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (NULL, 1, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0);

INSERT INTO buy_book(buy_id, book_id, amount, user_created, date_created, user_modified, date_modified, row_version)
VALUES (1, 1, 1, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (1, 7, 2, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (1, 3, 1, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (2, 8, 2, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (3, 3, 2, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (3, 2, 1, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (3, 1, 1, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (4, 5, 1, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0);

INSERT INTO step (name_step, user_created, date_created, user_modified, date_modified, row_version)
VALUES ('Оплата', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Упаковка', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Транспортировка', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       ('Доставка', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0);

INSERT INTO buy_step (buy_id, step_id, date_step_beg, date_step_end, user_created, date_created, user_modified, date_modified, row_version)
VALUES (1, 1, '2020-02-20', '2020-02-20', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (1, 2, '2020-02-20', '2020-02-21', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (1, 3, '2020-02-22', '2020-03-07', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (1, 4, '2020-03-08', '2020-03-08', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (2, 1, '2020-02-28', '2020-02-28', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (2, 2, '2020-02-29', '2020-03-01', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (2, 3, '2020-03-02', NULL, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (2, 4, NULL, NULL, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (3, 1, '2020-03-05', '2020-03-05', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (3, 2, '2020-03-05', '2020-03-06', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (3, 3, '2020-03-06', '2020-03-10', 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (3, 4, '2020-03-11', NULL, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (4, 1, '2020-03-20', NULL, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (4, 2, NULL, NULL, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (4, 3, NULL, NULL, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0),
       (4, 4, NULL, NULL, 0, '2024-10-29T16:07:25.690739+00:00', NULL, NULL, 0);
