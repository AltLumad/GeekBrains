/*Практическое задание по теме “Хранимые процедуры и функции, триггеры"*/
DELIMITER //


/*
1)Создайте хранимую функцию hello(), которая будет возвращать приветствие, 
в зависимости от текущего времени суток. 
С 6:00 до 12:00 функция должна возвращать фразу "Доброе утро", 
с 12:00 до 18:00 функция должна возвращать фразу "Добрый день",
с 18:00 до 00:00 — "Добрый вечер", с 00:00 до 6:00 — "Доброй ночи".
*/
SELECT "TASK 1"//
DROP FUNCTION IF EXISTS hello;
CREATE FUNCTION hello()
RETURNS TEXT DETERMINISTIC
BEGIN
    DECLARE tme TIMESTAMP; 
    SELECT DATE_FORMAT(NOW(), "%d.%m.%Y") INTO tme;
    CASE 
        WHEN tme BETWEEN '06:00:00' AND '12:00:00' THEN RETURN "Доброе утро"; 
        WHEN tme BETWEEN '12:00:00' AND '18:00:00' THEN RETURN "Добрый день"; 
		WHEN tme BETWEEN '18:00:00' AND '00:00:00' THEN RETURN "Добрый вечер"; 
        ELSE RETURN "Доброй ночи";  
    END CASE;
END//

/*
2)В таблице products есть два текстовых поля: name с названием товара и description с его описанием.
 Допустимо присутствие обоих полей или одно из них. 
 Ситуация, когда оба поля принимают неопределенное значение NULL неприемлема. 
 Используя триггеры, добейтесь того, чтобы одно из этих полей или оба поля были заполнены. 
 При попытке присвоить полям NULL-значение необходимо отменить операцию.*/
SELECT "TASK 2"//
DROP PROCEDURE IF EXISTS throw_error_if_true;
CREATE PROCEDURE throw_error_if_true(IN val BOOLEAN)
BEGIN
     DECLARE msg VARCHAR(50) DEFAULT "Only one field maybe NULL";

/*Как я понял если NEW == OLD то значение не поменялось => условие должно покрыть весь массив случаев*/

    IF (val) THEN 
        SIGNAL SQLSTATE '45001' SET MESSAGE_TEXT = msg;
    END IF;
END//
   
DROP TRIGGER IF EXISTS check_products_insert_not_null_fields;
CREATE TRIGGER check_products_insert_not_null_fields BEFORE INSERT ON products
FOR EACH ROW
BEGIN
    DECLARE chk BOOLEAN DEFAULT (NEW.name IS NULL AND NEW.description IS NULL);
    CALL throw_error_if_true(chk);
END//

DROP TRIGGER IF EXISTS check_products_update_not_null_fields;
CREATE TRIGGER check_products_update_not_null_fields BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
    DECLARE chk BOOLEAN DEFAULT (NEW.name IS NULL AND NEW.description IS NULL);
    CALL throw_error_if_true(chk);

END//
  
 
 /*
 3)(по желанию) Напишите хранимую функцию для вычисления произвольного числа Фибоначчи. 
 Числами Фибоначчи называется последовательность в которой число равно сумме двух предыдущих чисел. 
 Вызов функции FIBONACCI(10) должен возвращать число 55.*/
SELECT "TASK 3";
DROP FUNCTION IF EXISTS FIBONACCI; 
CREATE FUNCTION FIBONACCI(n INT)
RETURNS TEXT DETERMINISTIC
BEGIN
    DECLARE p1 INT DEFAULT 1;
    DECLARE p2 INT DEFAULT 1;
    DECLARE i INT DEFAULT 2;
    DECLARE res INT DEFAULT 0;
   
    IF (n <= 1) THEN RETURN n;
    ELSEIF (n = 2) THEN RETURN 1;
    END IF;  
    WHILE i < n DO
        SET i = i + 1;
	SET res = p2 + p1;
        SET p2 = p1;
        SET p1 = res;
    END WHILE;
    RETURN res;
 END//
 
DELIMITER ;
