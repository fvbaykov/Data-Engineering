REM   Script: Homework 1 Final Variant
REM   Homework due to 29-01-2022

create table client( 
    id integer primary key, 
    name varchar(64), 
    lastname varchar(64), 
    locator_id integer, 
    city varchar(64) 
    );

create table locators( 
    locator_id integer primary key, 
    phone varchar(20), 
    email varchar(64) 
    );

create table transactions( 
    id integer primary key, 
    client_id integer, 
    money_amount number(*, 2), 
    currency_id integer 
    );

create table currency_types( 
    id integer primary key, 
    title varchar(16) 
    );

create table currency_exchange( 
    id integer, 
    to_currency_id integer, 
    coef number(*, 3) 
    );

insert into client(id, name, lastname, locator_id, city) values(1, 'Александр', 'Иванов', 1, 'Уфа');

insert into client(id, name, lastname, locator_id, city) values(2, 'Борис', 'Калинин', 7, 'Ереван');

insert into client(id, name, lastname, locator_id, city) values(3, 'Петр', 'Суворов', 2, 'Казань');

insert into client(id, name, lastname, locator_id, city) values(4, 'Юрий', 'Сахаров', 6, 'Владимир');

insert into client(id, name, lastname, locator_id, city) values(5, 'Всеволод', 'Долгих', 4, 'Екатеринбург');

insert into client(id, name, lastname, locator_id, city) values(6, 'Александр', 'Виноградов', 5, 'Москва');

insert into client(id, name, lastname, locator_id, city) values(7, 'Николай', 'Николаев', 2, 'Нижний Новгород');

insert into client(id, name, lastname, locator_id, city) values(8, 'Ольга', 'Печуркина', 1, 'Санкт-Петербург');

insert into client(id, name, lastname, locator_id, city) values(9, 'Екатерина', 'Александрова', 8, 'Чебоксары');

insert into client(id, name, lastname, locator_id, city) values(10, 'Юлия', 'Абрикосова', 3, 'Москва');



insert into locators(locator_id, phone, email) values(1, '+7(495)563-83-79', 'ivan.92@mail.ru');

insert into locators(locator_id, phone, email) values(2, '+374(905)750-44-13', 'Nik.nik@mail.ru');

insert into locators(locator_id, phone, email) values(3, '+7(916)258-30-30', 'Apricot.Yla@mail.ru');

insert into locators(locator_id, phone, email) values(4, '+7(909)546-77-76', 'Dolg.Seva@mail.ru');

insert into locators(locator_id, phone, email) values(5, '+374(903)391-77-01', 'Vino.Sasha@mail.ru');

insert into locators(locator_id, phone, email) values(6, '+7(495)620-04-40', 'Sacharov.Yuri_13@mail.ru');

insert into locators(locator_id, phone, email) values(7, '+374(905)980-02-08', 'Bor.Kalin@mail.ru');

insert into locators(locator_id, phone, email) values(8, '+7(916)444-22-04', 'Katusha.93@mail.ru');



insert into transactions(id, client_id, money_amount, currency_id) values(1, 4, 16600, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(2, 5, 5, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(3, 7, 15000, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(4, 7, 14700, 3);

insert into transactions(id, client_id, money_amount, currency_id) values(5, 10, 50000, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(6, 7, 11000, 1);

insert into transactions(id, client_id, money_amount, currency_id) values(7, 2, 10900, 3);

insert into transactions(id, client_id, money_amount, currency_id) values(8, 6, 15400, 3);

insert into transactions(id, client_id, money_amount, currency_id) values(9, 5, 10800, 1);

insert into transactions(id, client_id, money_amount, currency_id) values(10, 7, 15100, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(11, 8, 7, 1);

insert into transactions(id, client_id, money_amount, currency_id) values(12, 5, 10400, 1);

insert into transactions(id, client_id, money_amount, currency_id) values(13, 5, 17700, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(14, 8, 15600, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(15, 3, 14600, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(16, 6, 13900, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(17, 4, 700000, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(18, 8, 13100, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(19, 6, 17000, 1);

insert into transactions(id, client_id, money_amount, currency_id) values(20, 10, 16700, 3);

insert into transactions(id, client_id, money_amount, currency_id) values(21, 3, 1000000, 3);

insert into transactions(id, client_id, money_amount, currency_id) values(22, 7, 17300, 1);

insert into transactions(id, client_id, money_amount, currency_id) values(23, 2, 15100, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(24, 7, 18600, 3);

insert into transactions(id, client_id, money_amount, currency_id) values(25, 3, 4, 1);

insert into transactions(id, client_id, money_amount, currency_id) values(26, 2, 18900, 2);

insert into transactions(id, client_id, money_amount, currency_id) values(27, 5, 13900, 1);

insert into transactions(id, client_id, money_amount, currency_id) values(28, 5, 14800, 3);

insert into transactions(id, client_id, money_amount, currency_id) values(29, 5, 17100, 1);

insert into transactions(id, client_id, money_amount, currency_id) values(30, 4, 16700, 3);



insert into currency_types(id, title) values(1, 'Рубль');

insert into currency_types(id, title) values(2, 'Доллар');

insert into currency_types(id, title) values(3, 'Евро');

insert into currency_exchange(id, to_currency_id, coef) values(1, 2, 0.013);

insert into currency_exchange(id, to_currency_id, coef) values(1, 3, 0.011);

insert into currency_exchange(id, to_currency_id, coef) values(2, 1, 76.01);

insert into currency_exchange(id, to_currency_id, coef) values(2, 3, 0.85);

insert into currency_exchange(id, to_currency_id, coef) values(3, 1, 89.88);

insert into currency_exchange(id, to_currency_id, coef) values(3, 2, 1.18);





select * from client where city = 'Москва';

select * from client where name like 'А%';

select * from locators where phone not like '+7%';

select * from transactions where currency_id in (1, 2);

select * from transactions where currency_id = 1 and money_amount not between 10 and 20000;

