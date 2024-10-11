--drop table task

create table task
(
    id integer not null primary key,
    name varchar not null,
    description varchar null
);

select * from task;
