-- Улчшаем запросы
-- Т.к. потоянно используется CONCAT(firstname, ' ', lastname) то добовляем вычисляемую колонку
ALTER TABLE users 
ADD COLUMN fullname VARCHAR(250)
GENERATED ALWAYS as  (CONCAT(firstname, ' ', lastname)) VIRTUAL;

-- Зачем везде писать = 1, когда можно назначить алиас таблице и обращаться уже по id
SELECT
  fullname,
  (SELECT filename FROM media WHERE id = 
    (SELECT photo_id FROM profiles WHERE user_id = U.id)
  )
  , (SELECT hometown FROM profiles WHERE user_id = U.id)
  FROM users AS U
    WHERE id = 1;  

-- аналогично запроосу выше
SELECT CONCAT(
  'Пользователь ', 
  (SELECT fullname  FROM users WHERE id=M.user_id),
  ' добавил фото ', 
  filename, ' ', 
  created_at) AS news 
    FROM media AS M
    WHERE user_id = 1 
      AND media_type_id = ( SELECT id FROM media_types WHERE name LIKE 'photo');


 -- Выводим не безликие id, а имя фамилию пользователя
(SELECT (select fullname FROM users where id = friend_id) as fullname FROM friendship WHERE user_id = 1)
UNION
(SELECT (select fullname FROM users where id = user_id)  FROM friendship WHERE friend_id = 1);

-- Объединяем медиафайлы пользователя и его друзей для создания ленты новостей
SELECT filename, (SELECT fullname from users WHERE id = user_id), created_at FROM media WHERE user_id = 1
UNION
SELECT filename, (SELECT fullname from users WHERE id = user_id), created_at FROM media WHERE user_id IN (
  (SELECT friend_id FROM friendship 
	WHERE user_id = 1
		AND confirmed_at IS NOT NULL 
		AND status IS NOT NULL
  ) UNION (
  SELECT user_id FROM friendship 
    WHERE friend_id = 1
      AND confirmed_at IS NOT NULL 
      AND status IS NOT NULL
  )
);


-- Убрали из сортировки месяцы в явном виде
SELECT COUNT(id) AS news, MONTHNAME(created_at) AS month 
  FROM media
  WHERE YEAR(created_at) = YEAR(NOW())
  GROUP BY month, MONTH(created_at)
  ORDER BY MONTH(created_at) DESC;

SELECT COUNT(id) AS news, MONTHNAME(created_at) AS month 
  FROM media
  WHERE YEAR(created_at) = YEAR(NOW())
  GROUP BY month, MONTH(created_at)
  ORDER BY MONTH(created_at) DESC;

SELECT COUNT(id) AS news, MONTHNAME(created_at) AS month 
  FROM media
  GROUP BY month, MONTH(created_at)
  ORDER BY MONTH(created_at) DESC;
      
  

  
