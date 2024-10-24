SET search_path TO books,public;

create table task
(
    id integer not null GENERATED ALWAYS AS IDENTITY primary key,
    name varchar(30) not null,
    description varchar(100) null
);

--select * from task;
