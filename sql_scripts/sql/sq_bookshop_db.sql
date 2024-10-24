/*
Before RUN delete all comments!

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

CREATE TABLE author
(
	author_id integer NOT NULL PRIMARY KEY,
	name_author varchar(30) NOT NULL
);

CREATE TABLE genre
(
	genre_id integer NOT NULL PRIMARY KEY,
	name_genre varchar(30) NOT NULL
);

CREATE TABLE book
(
	book_id integer NOT NULL PRIMARY KEY,
	title varchar(50) NOT NULL,
	author_id integer NOT NULL,
	genre_id integer NOT NULL,
	price decimal(10,2) NOT NULL,
	amount integer NOT NULL,
	FOREIGN KEY (author_id) REFERENCES author (author_id),
	FOREIGN KEY (genre_id) REFERENCES genre (genre_id)
);

CREATE TABLE city
(
	city_id integer NOT NULL PRIMARY KEY,
	name_city varchar(30) NOT NULL,
	days_delivery integer NOT NULL
);

CREATE TABLE client
(
	client_id integer NOT NULL PRIMARY KEY,
	name_client varchar(50) NOT NULL,
	city_id integer NOT NULL,
	email varchar(30) NOT NULL,
	FOREIGN KEY (city_id) REFERENCES city (city_id)
);

CREATE TABLE buy
(
	buy_id integer NOT NULL PRIMARY KEY,
	buy_description varchar(100) NULL,
	client_id integer NOT NULL,
	FOREIGN KEY (client_id) REFERENCES client (client_id)
);

CREATE TABLE step
(
	step_id integer NOT NULL PRIMARY KEY,
	name_step varchar(30) NOT NULL
);

CREATE TABLE buy_book
(
	buy_book_id integer NOT NULL PRIMARY KEY,
	buy_id integer NOT NULL,
	book_id integer NOT NULL,
	amount integer NOT NULL,
	FOREIGN KEY (buy_id) REFERENCES buy (buy_id),
	FOREIGN KEY (book_id) REFERENCES book (book_id)
);

CREATE TABLE buy_step
(
	buy_step_id integer NOT NULL PRIMARY KEY,
	buy_id integer NOT NULL,
	step_id integer NOT NULL,
	date_step_beg DATE,
	date_step_end DATE,
	FOREIGN KEY (buy_id) REFERENCES buy (buy_id),
	FOREIGN KEY (step_id) REFERENCES step (step_id)
);

INSERT INTO author (name_author)
VALUES ('Булгаков М.А.'),
       ('Достоевский Ф.М.'),
       ('Есенин С.А.'),
       ('Пастернак Б.Л.'),
       ('Лермонтов М.Ю.');

INSERT INTO genre (name_genre)
VALUES ('Роман'),
       ('Поэзия'),
       ('Приключения');

INSERT INTO book (title, author_id, genre_id, price, amount)
VALUES  ('Мастер и Маргарита', 1, 1, 670.99, 3),
        ('Белая гвардия ', 1, 1, 540.50, 5),
        ('Идиот', 2, 1, 460.00, 10),
        ('Братья Карамазовы', 2, 1, 799.01, 2),
        ('Игрок', 2, 1, 480.50, 10),
        ('Стихотворения и поэмы', 3, 2, 650.00, 15),
        ('Черный человек', 3, 2, 570.20, 6),
        ('Лирика', 4, 2, 518.99, 2);

INSERT INTO city (name_city, days_delivery)
VALUES ('Москва', 5),
       ('Санкт-Петербург', 3),
       ('Владивосток', 12);

INSERT INTO client (name_client, city_id, email)
VALUES ('Баранов Павел', 3, 'baranov@test'),
       ('Абрамова Катя', 1, 'abramova@test'),
       ('Семенонов Иван', 2, 'semenov@test'),
       ('Яковлева Галина', 1, 'yakovleva@test');

INSERT INTO buy (buy_description, client_id)
VALUES ('Доставка только вечером', 1),
       (NULL, 3),
       ('Упаковать каждую книгу по отдельности', 2),
       (NULL, 1);

INSERT INTO buy_book(buy_id, book_id, amount)
VALUES (1, 1, 1),
       (1, 7, 2),
       (1, 3, 1),
       (2, 8, 2),
       (3, 3, 2),
       (3, 2, 1),
       (3, 1, 1),
       (4, 5, 1);

INSERT INTO step (name_step)
VALUES ('Оплата'),
       ('Упаковка'),
       ('Транспортировка'),
       ('Доставка');

INSERT INTO buy_step (buy_id, step_id, date_step_beg, date_step_end)
VALUES (1, 1, '2020-02-20', '2020-02-20'),
       (1, 2, '2020-02-20', '2020-02-21'),
       (1, 3, '2020-02-22', '2020-03-07'),
       (1, 4, '2020-03-08', '2020-03-08'),
       (2, 1, '2020-02-28', '2020-02-28'),
       (2, 2, '2020-02-29', '2020-03-01'),
       (2, 3, '2020-03-02', NULL),
       (2, 4, NULL, NULL),
       (3, 1, '2020-03-05', '2020-03-05'),
       (3, 2, '2020-03-05', '2020-03-06'),
       (3, 3, '2020-03-06', '2020-03-10'),
       (3, 4, '2020-03-11', NULL),
       (4, 1, '2020-03-20', NULL),
       (4, 2, NULL, NULL),
       (4, 3, NULL, NULL),
       (4, 4, NULL, NULL);
