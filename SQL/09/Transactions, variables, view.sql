/*Практическое задание по теме “Транзакции, переменные, представления”*/
-----------------------------------------------------------------------------------
/*1)В базе данных shop и sample присутствуют одни и те же таблицы, учебной базы данных. 
Переместите запись id = 1 из таблицы shop.users в таблицу sample.users. Используйте транзакции.*/
USE sample;
START TRANSACTION;
INSERT INTO users SELECT * FROM shop.users WHERE id = 1;
DELETE FROM shop.users WHERE id = 1;
COMMIT;

-----------------------------------------------------------------------------------
/*2)Создайте представление, которое выводит название name товарной позиции из таблицы products 
и соответствующее название каталога name из таблицы catalogs.*/
CREATE VIEW pretty_catalog (product_name, catalog_name) AS
SELECT p.name, c.name FROM products p
	LEFT JOIN catalogs c ON c.id = p.catalog_id; -- LEFT JOIN использован намеренно, на мой взгляд даже если продукт не имеет ссылки на каталог, он должен выводиться.

-----------------------------------------------------------------------------------
/*3) по желанию) Пусть имеется таблица с календарным полем created_at. 
В ней размещены разряженые календарные записи за август 2018 года '2018-08-01', '2016-08-04', '2018-08-16' и 2018-08-17. 
Составьте запрос, который выводит полный список дат за август, выставляя в соседнем поле значение 1, 
если дата присутствует в исходном таблице и 0, если она отсутствует.*/
CREATE TABLE test_table (created_at DATETIME);
INSERT INTO test_table (created_at) 
VALUES ('2018-08-01'), ('2018-08-04'), ('2018-08-16'), ('2018-08-17'), ('2018-08-21'), ('2018-08-24');
SET @begindate := '2019-08-01';
WITH RECURSIVE T (dte, is_exist) AS 
(
SELECT @begindate,
       EXISTS(SELECT * FROM test_table WHERE created_at = @begindate)
UNION ALL
SELECT @begindate := @begindate + INTERVAL 1 DAY,
       EXISTS(SELECT * FROM test_table WHERE created_at = @begindate)
FROM T
WHERE @begindate < '2018-10-01'
)
SELECT * FROM T	   
-----------------------------------------------------------------------------------

/*4)(по желанию) Пусть имеется любая таблица с календарным полем created_at. 
Создайте запрос, который удаляет устаревшие записи из таблицы, оставляя только 5 самых свежих записей.*/
PREPARE delf FROM "DELETE FROM created_at ORDER BY created_at LIMIT ?";
SET @lim := (SELECT COUNT(*) -5 FROM created_at);
EXECUTE delf USING @lim;
