CREATE SCHEMA books;

CREATE TABLE books.author
(
	author_id int NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name_author varchar(30) NOT NULL
);

INSERT INTO books.author (name_author)
VALUES ('Булгаков М.А.'),
       ('Достоевский Ф.М.'),
       ('Есенин С.А.'),
       ('Пастернак Б.Л.'),
       ('Лермонтов М.Ю.');

CREATE TABLE books.genre
(
	genre_id int NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name_genre varchar(30) NOT NULL
);

INSERT INTO books.genre (name_genre)
VALUES ('Роман'),
       ('Поэзия'),
       ('Приключения');

CREATE TABLE books.book
(
	book_id int NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	title varchar(50) NOT NULL,
	author_id int NOT NULL,
	genre_id int NOT NULL,
	price decimal(10,2) NOT NULL,
	amount int NOT NULL
);

INSERT INTO books.book (title, author_id, genre_id, price, amount)
VALUES  ('Мастер и Маргарита', 1, 1, 670.99, 3),
        ('Белая гвардия ', 1, 1, 540.50, 5),
        ('Идиот', 2, 1, 460.00, 10),
        ('Братья Карамазовы', 2, 1, 799.01, 2),
        ('Игрок', 2, 1, 480.50, 10),
        ('Стихотворения и поэмы', 3, 2, 650.00, 15),
        ('Черный человек', 3, 2, 570.20, 6),
        ('Лирика', 4, 2, 518.99, 2);

CREATE TABLE books.city
(
	city_id int NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name_city varchar(30) NOT NULL,
	days_delivery int NOT NULL
);

INSERT INTO books.city (name_city, days_delivery)
VALUES ('Москва', 5),
       ('Санкт-Петербург', 3),
       ('Владивосток', 12);

CREATE TABLE books.client
(
	client_id int NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name_client varchar(50) NOT NULL,
	city_id int NOT NULL,
	email varchar(30) NOT NULL
);

INSERT INTO books.client (name_client, city_id, email)
VALUES ('Баранов Павел', 3, 'baranov@test'),
       ('Абрамова Катя', 1, 'abramova@test'),
       ('Семенонов Иван', 2, 'semenov@test'),
       ('Яковлева Галина', 1, 'yakovleva@test');


CREATE TABLE books.buy
(
	buy_id int NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	buy_description varchar(100) NOT NULL,
	client_id int NOT NULL
);

INSERT INTO books.buy (buy_description, client_id)
VALUES ('Доставка только вечером', 1),
       (NULL, 3),
       ('Упаковать каждую книгу по отдельности', 2),
       (NULL, 1);



CREATE TABLE books.buy_book
(
	buy_book_id int NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	buy_id int NOT NULL,
	book_id int NOT NULL,
	amount int NOT NULL
);

INSERT INTO books.buy_book(buy_id, book_id, amount)
VALUES (1, 1, 1),
       (1, 7, 2),
       (1, 3, 1),
       (2, 8, 2),
       (3, 3, 2),
       (3, 2, 1),
       (3, 1, 1),
       (4, 5, 1);

CREATE TABLE books.step
(
	step_id int NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name_step varchar(30) NOT NULL
);

INSERT INTO books.step (name_step)
VALUES ('Оплата'),
       ('Упаковка'),
       ('Транспортировка'),
       ('Доставка');

CREATE TABLE books.buy_step
(
	buy_step_id int NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	buy_id int NOT NULL,
	step_id int NOT NULL,
	date_step_beg DATE,
	date_step_end DATE
);

INSERT INTO books.buy_step (buy_id, step_id, date_step_beg, date_step_end)
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

ALTER TABLE books.book ADD FOREIGN KEY (author_id) REFERENCES books.author (author_id);
ALTER TABLE books.book ADD FOREIGN KEY (genre_id) REFERENCES books.genre (genre_id);
ALTER TABLE books.client ADD FOREIGN KEY (city_id) REFERENCES books.city (city_id);
ALTER TABLE books.buy ADD FOREIGN KEY (client_id) REFERENCES books.client (client_id);
ALTER TABLE books.buy_step ADD FOREIGN KEY (buy_id) REFERENCES books.buy (buy_id);
ALTER TABLE books.buy_step ADD FOREIGN KEY (step_id) REFERENCES books.step (step_id);
ALTER TABLE books.buy_book ADD FOREIGN KEY (buy_id) REFERENCES buy.step (buy_id);
ALTER TABLE books.buy_book ADD FOREIGN KEY (book_id) REFERENCES book.step (book_id);


SELECT * FROM books.author;
SELECT * FROM books.genre;
SELECT * FROM books.book;
SELECT * FROM books.city;
SELECT * FROM books.client;
SELECT * FROM books.step;
SELECT * FROM books.buy;
SELECT * FROM books.buy_step;
SELECT * FROM books.buy_book;
