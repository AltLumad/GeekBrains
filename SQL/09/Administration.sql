/*Практическое задание по теме “Администрирование MySQL” (эта тема изучается по вашему желанию)*/

USE shop;
/*1)Создайте двух пользователей которые имеют доступ к базе данных shop. 
Первому пользователю shop_read должны быть доступны только запросы на чтение данных, 
второму пользователю shop — любые операции в пределах базы данных shop.*/

DROP USER IF EXISTS shop;
CREATE USER shop IDENTIFIED WITH sha256_password BY '123';
GRANT ALL ON shop.* TO shop;

DROP USER IF EXISTS shop_read;
CREATE USER shop_read IDENTIFIED WITH sha256_password BY '123';
GRANT SELECT ON shop.* TO shop_read;

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

DROP USER IF EXISTS shop_read;
CREATE USER shop_read;
GRANT SELECT ON shop.accounts TO shop_read;