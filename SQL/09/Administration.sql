/*Практическое задание по теме “Администрирование MySQL” (эта тема изучается по вашему желанию)*/

USE shop;
/*1)Создайте двух пользователей которые имеют доступ к базе данных shop. 
Первому пользователю shop_read должны быть доступны только запросы на чтение данных, 
второму пользователю shop — любые операции в пределах базы данных shop.*/

CREATE USER shop_read;
CREATE USER shop;
GRANT SELECT ON shop.* TO shop_read;
GRANT ALL ON shop.* TO shop;
/*2)(по желанию) Пусть имеется таблица accounts содержащая три столбца id, name, password, 
содержащие первичный ключ, имя пользователя и его пароль. 
Создайте представление username таблицы accounts, предоставляющий доступ к столбца id и name. 
Создайте пользователя user_read, который бы не имел доступа к таблице accounts, однако
, мог бы извлекать записи из представления username.*/

DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
	id SERIAL PRIMARY KEY,
	name VARCHAR (50),
	password VARCHAR(50)
);

CREATE VIEW username(id, name) AS
SELECT id, name FROM accounts;

CREATE USER shop_read;
GRANT SELECT ON shop.accounts TO shop_read;