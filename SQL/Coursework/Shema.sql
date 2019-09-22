/*
***Требования к курсовому проекту:

общее текстовое описание БД и решаемых ею задач;
создать ERDiagram для БД;
скрипты характерных выборок (включающие группировки, JOIN'ы, вложенные таблицы);
представления (минимум 2);
хранимые процедуры / триггеры;*/
DROP DATABASE IF EXISTS dba;
CREATE DATABASE dba;
USE dba;

-- Пользователи----------------------------------------------
CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	firstname VARCHAR(100),
	lastname VARCHAR(100),
	login VARCHAR(25) UNIQUE,
	password VARCHAR(128),  -- Хеш паролей, 
	email VARCHAR(50) UNIQUE
);
ALTER TABLE users 
ADD COLUMN fullname VARCHAR(200) 
GENERATED ALWAYS as (CONCAT(firstname, ' ', lastname));

-- Следим что бы точно в БД попал в хеш. Даже если клиентское приложение тоже будет кешировать пароль, то получится кеш от кеша, и ничего страшного не произойдет.
DELIMITER //
CREATE TRIGGER users_insert_trg BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    SET NEW.password = MD5(NEW.password);
END//
DELIMITER ;

CREATE TABLE profilies (
	user_id INT NOT NULL PRIMARY KEY,
	birthdate DATE NOT NULL,
	pasport_numer VARCHAR(50)
);

ALTER TABLE profilies
ADD CONSTRAINT fk_profile_user_id
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

DELIMITER //
CREATE PROCEDURE check_user_pass(IN login_ VARCHAR(25), IN password_ VARCHAR(128))
BEGIN
	DECLARE has_user BOOLEAN;
	SET has_user = EXISTS(SELECT * FROM users WHERE login = login_ and password = MD5(password_));
    IF (has_user = FALSE) THEN 
        SIGNAL SQLSTATE '45001' SET MESSAGE_TEXT = "Wrong login/password";
    END IF;
END//
DELIMITER ;
/*------------------------------------------------------------------------*/

/*--------Организации-----------------------------------------------------------*/
CREATE TABLE organization(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR (100) NOT NULL,
	parent_id INT DEFAULT NULL
);

ALTER TABLE organization
ADD CONSTRAINT fk_organization_parent_id
FOREIGN KEY (parent_id)
REFERENCES organization(id)
ON DELETE SET NULL
ON UPDATE CASCADE;
/*------------------------------------------------------------------------*/

/*--------Таблица типов владельцев-----------------------------------------------------------*/
CREATE TABLE owner_type (
	id INT AUTO_INCREMENT PRIMARY KEY,
	typename VARCHAR(200)
);
/*------------------------------------------------------------------------*/

/*-----------------Телефоны и реквизиты пользователей и компаний--------------------*/
CREATE TABLE phones (
	phone VARCHAR(25) PRIMARY KEY,
	owner_id INT NOT NULL,
	owner_type_id INT NOT NULL
);
	
ALTER TABLE phones
ADD CONSTRAINT fk_phones_owner_type_id
FOREIGN KEY (owner_type_id)
REFERENCES owner_type (id)
ON DELETE CASCADE
ON UPDATE CASCADE;


CREATE TABLE requisites (
	owner_id INT NOT NULL,
	owner_type_id INT NOT NULL,
	inn VARCHAR(12) NOT NULL,
	kpp VARCHAR(12),
	PRIMARY KEY (owner_id,owner_type_id), 
	CONSTRAINT inn_kpp UNIQUE (inn,kpp)
);

ALTER TABLE requisites
ADD CONSTRAINT fk_requisites_owner_type_id
FOREIGN KEY (owner_type_id)
REFERENCES owner_type (id)
ON DELETE CASCADE
ON UPDATE CASCADE;
/*------------------------------------------------------------------------*/

/*-----------------Валюты и курс----------------------------------------*/


CREATE TABLE currency (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE,
	signs VARCHAR(5) NOT NULL UNIQUE,
	CODE VARCHAR(5) NOT NULL UNIQUE
);

-- Такой подход создаёт дублирование данных, но даже если программа проработает 30 лет, то для 10 валют это будет всего ~ 220 000 записей
-- Это не много и не имеет смысла сильно усложнять логику.
CREATE TABLE currency_date ( 
	currency1_id INT NOT NULL,
	currency2_id INT NOT NULL,
	curdate DATE,
	rate NUMERIC(20,4),
	PRIMARY KEY (currency1_id,currency2_id, curdate) 
);

ALTER TABLE currency_date
ADD CONSTRAINT fk_currency_date_currency1_id
FOREIGN KEY (currency1_id)
REFERENCES currency (id)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE currency_date
ADD CONSTRAINT fk_currency_date_currency2_id
FOREIGN KEY (currency2_id)
REFERENCES currency (id)
ON DELETE CASCADE
ON UPDATE CASCADE;


DELIMITER //
CREATE FUNCTION GetRate(currency1_ INT, currency2_ INT, curdate_ DATE)
RETURNS NUMERIC(20, 4) READS SQL DATA
BEGIN
  	DECLARE res NUMERIC(20,4);
  	SET res = 
  	    (SELECT rate 
  	     FROM currancy_date 
  	     WHERE currency1 = currency1_
  	       and currency2 = currency2_
  	       and curdate = curdate_
  	     );
    RETURN res;
END//
DELIMITER ;



/*------------------------------------------------------------------------*/



/*--------------------------------Счета------------------------------------*/
CREATE TABLE accounts (
	id INT AUTO_INCREMENT PRIMARY KEY,
	account NUMERIC NOT NULL UNIQUE,
	currency_id INT NOT NULL,
	owner_id INT NOT NULL,
	owner_type_id INT NOT NULL,
	name VARCHAR(100) NOT NULL UNIQUE
);

ALTER TABLE accounts
ADD CONSTRAINT fk_accounts_currency_id
FOREIGN KEY (currency_id)
REFERENCES currency(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE accounts
ADD CONSTRAINT fk_accounts_owner_type_id
FOREIGN KEY (owner_type_id)
REFERENCES owner_type (id)
ON DELETE CASCADE
ON UPDATE CASCADE;
/*------------------------------------------------------------------------*/


/*------------------------Транзакции-------------------------------------*/
CREATE TABLE transactions (
	id INT AUTO_INCREMENT PRIMARY KEY,
	ammount NUMERIC(20,4) NOT NULL,
	opdate DATETIME NOT NULL,
	created_at DATETIME DEFAULT NOW(),
	updated_at DATETIME DEFAULT NOW() ON UPDATE NOW(),
	payment_from INT NOT NULL,
	payment_to INT NOT NULL,
	UNIQUE(opdate, payment_from, payment_to)
); 

ALTER TABLE transactions
ADD CONSTRAINT fk_transactions_payment_from
FOREIGN KEY (payment_from)
REFERENCES accounts(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE transactions
ADD CONSTRAINT fk_transactions_payment_to
FOREIGN KEY (payment_to)
REFERENCES accounts(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

CREATE INDEX transactions_opdate_idx ON transactions(opdate); -- Очевидно, что часто будет требоваться выборка за дату или период.
CREATE INDEX transactions_payment_from_idx ON transactions(payment_from); -- Индекс требуется для выписке по счётуы
/*---------------------------------------------------------------------------*/

/*--------------------Аналитики, типы аналитик, значения аналитик------------------------------------------*/
CREATE TABLE analytic_types (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50)
);

CREATE TABLE analytics (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50),
	type_id int NOT NULL
);

ALTER TABLE analytics
ADD CONSTRAINT fk_analytics_type_id
FOREIGN KEY (type_id)
REFERENCES analytic_types(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

CREATE TABLE transactions_analytics (
	transaction_id INT NOT NULL,
	analytic_id INT NOT NULL,
	analytic_value BLOB,
	PRIMARY KEY(transaction_id, analytic_id)
);

ALTER TABLE transactions_analytics
ADD CONSTRAINT fk_transactions_analytics_transaction_id
FOREIGN KEY (transaction_id)
REFERENCES transactions(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE transactions_analytics
ADD CONSTRAINT fk_transactions_analytics_analytic_id
FOREIGN KEY (analytic_id)
REFERENCES analytics(id)
ON DELETE CASCADE
ON UPDATE CASCADE;
/*------------------------------------------------------------------------*/

/*-----------PROCEDURES--------------------------------*/
DELIMITER //
CREATE PROCEDURE pretty_transaction_by_period(IN begindate DATE, IN enddate DATE)
BEGIN
	SELECT   AFrom.name from_account , ATo.name to_account
           , T.ammount*GetRate(AFrom.currency_id, ATo.currency_id, T.opdate) ammount
           , C.signs  currency_to
    FROM transactions T 
        LEFT JOIN accounts AFrom 
            ON AFrom.id = T.payment_from
        LEFT JOIN accounts ATo 
            ON ATo.id = T.payment_to
        LEFT JOIN currency C
            ON C.id = ATo.currency_id
    WHERE T.opdate BETWEEN begindate AND enddate
END//
DELIMITER ;


/*------ VIEW------------------------*/
/*-----Списсок транзакций за сегодня-------*/
/*CREATE VIEW transactions_today (from_account, to_account, ammount, currency_from) AS
    SELECT   AFrom.name, ATo.name
           , T.ammount*GetRate(AFrom.currency_id, ATo.currency_id, T.opdate)
           , C.signs  
    FROM transactions T 
        LEFT JOIN accounts AFrom 
            ON AFrom.id = T.payment_from
        LEFT JOIN accounts ATo 
            ON ATo.id = T.payment_to
        LEFT JOIN currency C
            ON C.id = ATo.currency_id
    WHERE CAST(T.opdate as DATE) = CAST(NOW() AS DATE);*/
/*-----------------------------------------------------------------------------*/        

	
	