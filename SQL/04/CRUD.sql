--Create opearation
INSERT INTO (firstname, lastname, email, phone) 
VALUES  ('IVAN', 'Ivanov', 'ivan@mail.ivan', '8 800 555 35 35'),
        ('Petr', 'Petrov', 'petr@petrov.ru', '+7 999 888 77 66');


--Read opearations
SELECT * FROM users LIMIT 10;
SELECT DISTINCT firstname FROM users;
SELECT user_id, created_at FROM likes WHERE like_type_id = 1 and is_positive = TRUE;


--Update operations
UPDATE users
SET id = id + 1
WHERE id > 100;

--DELETE operations
DELETE FROM users
WHERE id > 100;

