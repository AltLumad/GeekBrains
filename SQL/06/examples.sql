-- Урок 6
-- Операторы, фильтрация, сортировка и ограничение

-- ДЗ вариант Игоря Самойленко
-- Тема 3, задание 1

/*
 * Пусть в таблице users поля created_at и updated_at оказались незаполненными. 
 * Заполните их текущими датой и временем.
 */

UPDATE users
   SET created_at=NOW(), updated_at=NOW();
   
  
UPDATE
  users
SET
  created_at = IF(created_at IS NULL, NOW(), created_at),
  updated_at = NOW();
  
-- Тема 3, задание 2

/*
 * Таблица users была неудачно спроектирована. 
 * Записи created_at и updated_at были заданы типом VARCHAR и в них долгое время 
 * помещались значения в формате "20.10.2017 8:10". 
 * Необходимо преобразовать поля к типу DATETIME, сохранив введеные ранее значения.
 */ 

UPDATE users
   SET created_at = str_to_date(created_at, '%d.%m.%Y %h:%i'), 
       updated_at = str_to_date(updated_at, '%d.%m.%Y %h:%i');

ALTER TABLE users 
	 MODIFY created_at DATETIME DEFAULT NOW(),
	 MODIFY updated_at DATETIME;
  
 -- Тема 3, задание 3

/*
 * В таблице складских запасов storehouses_products в поле value 
 * могут встречаться самые разные цифры: 0, если товар закончился и выше нуля, 
 * если на складе имеются запасы. Необходимо отсортировать записи таким образом, 
 * чтобы они выводились в порядке увеличения значения value. 
 * Однако, нулевые запасы должны выводиться в конце, после всех записей.
 */

SELECT * 
    FROM storehouses_products 
ORDER BY 
      IF(value = 0, 1, 0), value;
      

SELECT 
  * 
FROM storehouses_products 
ORDER BY value = 0, value;

-- Еще вариант решения:
SELECT 
  * 
FROM storehouses_products 
ORDER BY value <> 0 DESC, value;

-- Тема 3, задание 4

/*
 * (по желанию) Из таблицы users необходимо извлечь пользователей, 
 * родившихся в августе и мае. 
 * Месяцы заданы в виде списка английских названий ('may', 'august')
*/

SELECT *
  FROM users 
 WHERE DATE_FORMAT(birthday_at, "%M") IN('may', 'august');

SELECT 
  * 
FROM users 
WHERE MONTHNAME(birthday_at) IN ('May', 'August');

-- Тема 3, задание 5

/*
 * (по желанию) Из таблицы catalogs извлекаются записи при помощи запроса. 
 * SELECT * FROM catalogs WHERE id IN (5, 1, 2); 
 * Отсортируйте записи в порядке, заданном в списке IN.
*/

SELECT *
    FROM catalogs 
   WHERE id IN (5, 1, 2) 
ORDER BY FIELD(id, 5, 1, 2);


-- Тема 4, задание 1

/*
 * Подсчитайте средний возраст пользователей в таблице users
 */

SELECT AVG(TIMESTAMPDIFF(YEAR, birthday_at, NOW())) AS 'Средний возраст' 
	  FROM users;

/*
 * Подсчитайте количество дней рождения, которые приходятся на каждую из дней недели. 
 * Следует учесть, что необходимы дни недели текущего года, а не года рождения.
 */
 
SELECT DAYNAME(DATE_FORMAT(created_at, '2019-%m-%d')) as dayweek,
   COUNT(*)
    FROM users
GROUP BY dayweek;

SELECT
  CASE WEEKDAY(birthday_at)
    WHEN 0 THEN 'Понедельник'
    WHEN 1 THEN 'Вторник'
    WHEN 2 THEN 'Среда'
    WHEN 3 THEN 'Четверг'
    WHEN 4 THEN 'Пятница'
    WHEN 5 THEN 'Суббота'
    WHEN 6 THEN 'Воскресенье'
    ELSE -1
  END as wd,
  COUNT(birthday_at) as num
FROM users
GROUP BY wd
ORDER BY FIELD(wd,'Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье');


SELECT
  DATE_FORMAT(DATE(CONCAT_WS('-', YEAR(NOW()), MONTH(birthday_at), DAY(birthday_at))), '%W') AS day,
  COUNT(*) AS total
FROM
  users
GROUP BY
  day
ORDER BY
  total DESC;


/*
 * (по желанию) Подсчитайте произведение чисел в столбце таблицы
*/

# На основе формулы Бине
SELECT ROUND(EXP(SUM(LN(value)))) FROM tab3;


-- Примеры на основе базы данных vk
USE vk;

-- Получаем данные пользователя
SELECT * FROM users WHERE id=1;

SELECT firstname, lastname, 'main_photo', 'city' FROM users WHERE id=1;

SELECT
  firstname,
  lastname,
  (SELECT filename FROM media WHERE id = 
    (SELECT photo_id FROM profiles WHERE user_id = 1)
  ),
  (SELECT hometown FROM profiles WHERE user_id = 1)
  FROM users
    WHERE id = 1;           

-- Получаем фотографии пользователя
SELECT filename FROM media
  WHERE user_id = 1
    AND media_type_id = (
      SELECT id FROM media_types WHERE name LIKE '%photo%'
    );

-- Выбираем историю по добавлению фотографий пользователем
SELECT CONCAT(
  'Пользователь добавил фото ', 
  filename, 
  ' ', 
  created_at) AS news 
    FROM media 
    WHERE user_id = 1 
      AND media_type_id = (
        SELECT id FROM media_types WHERE name LIKE 'photo'
);

-- Улучшаем запрос
SELECT CONCAT(
  'Пользователь ', 
  (SELECT CONCAT(firstname, ' ', lastname)
    FROM users WHERE id=1),
  ' добавил фото ', 
  filename, ' ', 
  created_at) AS news 
    FROM media 
    WHERE user_id = 1 
      AND media_type_id = (
        SELECT id FROM media_types WHERE name LIKE 'photo'
);

-- Найдём кому принадлежат 10 самых больших медиафайлов
SELECT user_id, filename, size 
  FROM media 
  ORDER BY size DESC
  LIMIT 10;

-- Улучшим запрос
SELECT 
  filename, 
  size,
  (SELECT CONCAT(firstname, ' ', lastname) 
    FROM users u 
      WHERE u.id = m.user_id) AS owner 
  FROM media m
  ORDER BY size DESC
  LIMIT 10;
  
 -- Выбираем друзей пользователя
(SELECT friend_id FROM friendship WHERE user_id = 1)
UNION
(SELECT user_id FROM friendship WHERE friend_id = 1);

-- Выбираем только друзей с подтверждённым статусом
(SELECT friend_id 
  FROM friendship 
  WHERE user_id = 1
    AND confirmed_at IS NOT NULL 
    AND status IS NOT NULL
)
UNION
(SELECT user_id 
  FROM friendship 
  WHERE friend_id = 1
    AND confirmed_at IS NOT NULL 
    AND status IS NOT NULL
);


-- Выбираем медиафайлы друзей
SELECT filename FROM media WHERE user_id IN (
  (SELECT friend_id 
  FROM friendship 
  WHERE user_id = 1
    AND confirmed_at IS NOT NULL 
    AND status IS NOT NULL
  )
  UNION
  (SELECT user_id 
    FROM friendship 
    WHERE friend_id = 1
      AND confirmed_at IS NOT NULL 
      AND status IS NOT NULL
  )
);

-- Объединяем медиафайлы пользователя и его друзей для создания ленты новостей
SELECT filename, user_id, created_at FROM media WHERE user_id = 1
UNION
SELECT filename, user_id, created_at FROM media WHERE user_id IN (
  (SELECT friend_id 
  FROM friendship 
  WHERE user_id = 1
    AND confirmed_at IS NOT NULL 
    AND status IS NOT NULL
  )
  UNION
  (SELECT user_id 
    FROM friendship 
    WHERE friend_id = 1
      AND confirmed_at IS NOT NULL 
      AND status IS NOT NULL
  )
);

-- Определяем пользователей, общее занимаемое место медиафайлов которых 
-- превышает 1МБ

SELECT user_id, SUM(size) AS total
  FROM media
  GROUP BY user_id
  HAVING total > 1000
  ORDER BY total DESC;

-- Подсчитываем лайки для медиафайлов пользователя и его друзей

SELECT item_id AS mediafile, COUNT(*) AS likes 
  FROM likes 
    WHERE item_id IN (
      SELECT id FROM media WHERE user_id = 1
        UNION
      SELECT id FROM media WHERE user_id IN (
        SELECT friend_id 
          FROM friendship 
            WHERE user_id = 1 AND status IS NOT NULL)
)
GROUP BY item_id;

-- Начинаем создавать архив новостей для медиафайлов по месяцам
SELECT COUNT(id) AS arhive, MONTHNAME(created_at) AS month 
  FROM media
  GROUP BY month;
  
-- Архив с правильной сортировкой новостей по месяцам
SELECT COUNT(id) AS news, MONTHNAME(created_at) AS month 
  FROM media
  WHERE YEAR(created_at) = YEAR(NOW())
  GROUP BY month
  ORDER BY FIELD(month, 
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December') DESC;

SELECT COUNT(id) AS news, MONTHNAME(created_at) AS month 
  FROM media
  WHERE YEAR(created_at) = YEAR(NOW())
  GROUP BY month
  ORDER BY FIELD(month, 
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December') DESC;

SELECT COUNT(id) AS news, MONTHNAME(created_at) AS month 
  FROM media
  GROUP BY month
  ORDER BY FIELD(month, 
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December') DESC;
    

-- Выбираем сообщения от пользователя и к пользователю
SELECT from_user_id, to_user_id, body, delivered, created_at 
  FROM messages
    WHERE from_user_id = 1
      OR to_user_id = 1
    ORDER BY created_at DESC;
    
-- Непрочитанные сообщения
SELECT from_user_id, 
  to_user_id, 
  body, 
  IF(delivered, 'delivered', 'not delivered') AS status 
    FROM messages
      WHERE to_user_id = 2
        AND delivered IS NOT TRUE
    ORDER BY created_at DESC;
    
 -- Выводим друзей пользователя с преобразованием пола и возраста 
SELECT 
    (SELECT CONCAT(firstname, ' ', lastname) 
      FROM users 
      WHERE id = user_id) AS friend, 
      
    CASE (sex)
      WHEN 'm' THEN 'man'
      WHEN 'f' THEN 'women'
    END AS sex,
    
    TIMESTAMPDIFF(YEAR, birthday, NOW()) AS age
     
  FROM profiles
  
  WHERE user_id IN (
    SELECT friend_id 
    
      FROM friendship
      WHERE user_id = 1
        AND confirmed_at IS NOT NULL
        AND status IS NOT NULL
  );
    
-- Поиск пользователя по шаблонам имени  
SELECT CONCAT(firstname, ' ', lastname) AS fullname  
  FROM users
  HAVING fullname LIKE 'M%';
  
-- Используем регулярные выражения
SELECT CONCAT(firstname, ' ', lastname) AS fullname  
  FROM users
  HAVING fullname RLIKE '^M.*s$';
  
  

  
