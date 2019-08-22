/*(по желанию) Пусть имеется таблица рейсов flights (id, from, to) 
и таблица городов cities (label, name). 
Поля from, to и label содержат английские названия городов, 
поле name — русское. 
Выведите список рейсов flights с русскими названиями городов*/

CREATE DATABASE airlogs;
USE airlogs;


CREATE TABLE cities (
	label VARCHAR(100) PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);
INSERT INTO cities(label, name)
VALUE ('moscow','Москва'),('irkutsk','Иркутск'),
	  ('novgorod','Новгород'),('kazan','Казань'),
	  ('omsk','Омск'),('orsk','Орск');

CREATE TABLE flights (
	id SERIAL PRIMARY KEY,
	from VARCHAR(100) NOT NULL,
	to VARCHAR(100) NOT NULL
);
ALTER TABLE flights
ADD CONSTRAINT fk_from
FOREIGN KEY (from)
REFERENCES cities (label)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE flights
ADD CONSTRAINT fk_to
FOREIGN KEY (to)
REFERENCES cities (label)
ON DELETE CASCADE
ON UPDATE CASCADE;

INSERT INTO flights(from, to)
VALUE ('moscow','omsk'),('irkutsk','kazan'),
	  ('irkutsk','moscow'),('omsk','irkutsk'),
	  ('moscow','kazan'),('orsk','moscow');


