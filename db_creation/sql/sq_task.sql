create table task
(
    id integer not null primary key,
    name varchar(30) not null,
    description varchar(100) null
);

INSERT INTO task (name, description)
VALUES ('task 01 read an article', 'about our site'),
       ('task 02 write comment', NULL),
       ('task 03 add function', 'that adds new element to the list');

select * from task;
