/*
***Требования к курсовому проекту:

общее текстовое описание БД и решаемых ею задач;
минимальное количество таблиц - 10;
скрипты создания структуры БД (с первичными ключами, индексами, внешними ключами);
создать ERDiagram для БД;
скрипты наполнения БД данными;
скрипты характерных выборок (включающие группировки, JOIN'ы, вложенные таблицы);
представления (минимум 2);
хранимые процедуры / триггеры;*/
DROP DATABASE IF EXISTS dba;
CREATE DATABASE dba;
USE dba;
/*----Пользователи----------------------------------------------*/
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	firstname VARCHAR(100),
	lastname VARCHAR(100),
	login VARCHAR(25) UNIQUE,
	password VARCHAR(128),  -- Хеш паролей, 
	email VARCHAR(50) UNIQUE
);
ALTER TABLE users 
ADD COLUMN fullname VARCHAR(200) 
GENERATED ALWAYS as (CONCAT(firstname, ' ', lastname));

--Следим что бы точно в БД попал в хеш. Даже если клиентское приложение тоже будет кешировать пароль, то получится кеш от кеша, и ничего страшного не произойдет.
DELIMITER //
CREATE TRIGGER insert BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    NEW.password = MD5(NEW.password);
END//
DELIMITER ;

CREATE TABLE profilies (
	user_id INT NOT NULL PRIMARY KEY,
	birthdate DATE NOT NULL,
	pasport_numer VARCHAR(50),
);

ALTER TABLE profilies
ADD CONSTRAINT fk_profile_user_id
FOREIGN KEY (user_id)
REFERENCES users (id)
ON DELETE CASCADE
ON UPDATE CASCADE;


CREATE PROCEDURE check_user_pass(IN login_ VARCHAR(25), IN password_ VARCHAR(128))
BEGIN
	DECLARE has_user BOOLEAN;
	set has_user = EXISTS(SELECT * FROM users WHERE login = login_ and password = MD5(password_));
    IF (has_user = FALSE) THEN 
        SIGNAL SQLSTATE '45001' SET MESSAGE_TEXT = "Wrong login/password";
    END IF;
END//
/*------------------------------------------------------------------------*/

/*--------Организации-----------------------------------------------------------*/
CREATE TABLE organization(
	id SERIAL PRIMARY KEY,
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
	id SERIAL PRIMARY KEY,
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
	PRIMARY KEY (owner_id,owner_type), 
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
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE,
	signs VARCHAR(5) NOT NULL UNIQUE,
	CODE VARCHAR(5) NOT NULL UNIQUE
);

CREATE TABLE currency_date (
	currency1_id INT NOT NULL,
	currency2_id INT NOT NULL,
	curdate DATE,
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
/*------------------------------------------------------------------------*/



/*--------------------------------Счета------------------------------------*/
CREATE TABLE accounts (
	id SERIAL PRIMARY KEY,
	account NUMERIC NOT NULL UNIQUE,
	currency_id INT NOT NULL,
	owner_id INT NOT NULL,
	owner_type_id VARCHAR(50) NOT NULL,
	name VARCHAR(100) NOT NULL
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
	id SERIAL PRIMARY KEY,
	ammount NUMERIC(20,4) NOT NULL,
	opdate DATETIME NOT NULL,
	created_at DATETIME DEFAULT NOW(),
	updated_at DATETIME DEFAULT NOW() ON UPDATE NOW()
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
/*---------------------------------------------------------------------------*/

/*--------------------Аналитики, типы аналитик, значения аналитик------------------------------------------*/
CREATE TABLE analytic_types (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50),	
);

CREATE TABLE analytics (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50),
	type_id int NOT NULL
);

ALTER TABLE analytics
ADD CONSTRAINT fk_analytics_type_id
FOREIGN KEY (payment_to)
REFERENCES accounts(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

CREATE TABLE transactions_analytics (
	transaction_id INT NOT NULL,
	analytic_id INT NOT NULL,
	analytic_value BLOB,
	PRIMARY KEY(transaction_id, analytic_id)
);

ALTER TABLE analytics
ADD CONSTRAINT fk_analytics_type_id
FOREIGN KEY (payment_to)
REFERENCES accounts(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE analytics
ADD CONSTRAINT fk_analytics_type_id
FOREIGN KEY (payment_to)
REFERENCES accounts(id)
ON DELETE CASCADE
ON UPDATE CASCADE;
/*------------------------------------------------------------------------*/


	
	