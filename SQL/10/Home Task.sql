Задания на БД vk:
/*1. Проанализировать какие запросы могут выполняться наиболее часто в процессе работы приложения и добавить необходимые индексы.*/

-- Дабавим индекс из урока
CREATE INDEX media_user_id_media_type_id_idx ON media (user_id, media_type_id);  

-- часто просматривают друзей пользователя, добавляем два индекса
CREATE INDEX friendship_user_id_friend_id_idx ON media (user_id, friend_id);
CREATE INDEX friendship_friend_id_user_id_idx ON media (friend_id, user_id);

-- Лайкуют много, и люди любят просматривать кто-что лайкнул
CREATE INDEX likes_user_id_target_id_like_type_id_idx ON media (user_id, target_id, like_type_id);

-- Сообщений всегда очень много. Вся история переписки с другом заслуживает индекса. 
CREATE INDEX messages_from_user_id_to_user_id_created_at_idx ON media (from_user_id, to_user_id, created_at);
CREATE INDEX messages_to_user_id_from_user_id_created_at_idx ON media (to_user_id, from_user_id, created_at);

-- Пользователи ищут слова по все переписке, хочется добавить индекс на поле body. 
-- Однако это будет не хорошо, слишком большое поле. 
-- Нужно будет искать другие решения для ускорения выборки по телу сообщения 

-- Возможно имело бы смысл поставить индексы на: город+пользователь, город+пол, на fullname и т.д. но, без статистики такие решения лучше не принимать.


/*2. Задание на денормализацию
Разобраться как построен и работает следующий запрос:

SELECT SUM(count) as overall FROM (
    SELECT 
	    CONCAT(u.firstname, ' ', u.lastname) as user,
        count(l.id) as count,
        TIMESTAMPDIFF(YEAR, p.birthday, NOW()) AS age
    FROM users AS u
        INNER JOIN profiles AS p
            ON p.user_id = u.id
        LEFT JOIN media as m
            ON m.user_id = u.id
        LEFT JOIN messages as t
            ON t.from_user_id = u.id
        LEFT JOIN likes AS l
            ON l.item_id = u.id 
			   AND l.like_type_id = 2
               OR l.item_id = m.id AND l.like_type_id = 1
               OR l.item_id = t.id AND l.like_type_id = 3
    GROUP BY u.id
    ORDER BY p.birthday DESC
LIMIT 10) AS likes;

Правильно-ли он построен?
Какие изменения, включая денормализацию, можно внести в структуру БД
чтобы существенно повысить скорость работы этого запроса?*/

-- Запрос выводит сумму лайков у 10 самых молодых пользователей
-- Перенесём подзапрос для удобства в конструкцию with и уберем лишнее из select
-- Что бы не было путаницы поменяем alias у табли и стобцов
WITH rate_likes as (
    SELECT 
        count(l.id) as rate
    FROM users AS u
        INNER JOIN profiles AS p
            ON p.user_id = u.id
        LEFT JOIN media as m
            ON m.user_id = u.id
        LEFT JOIN messages as t
            ON t.from_user_id = u.id
        LEFT JOIN likes AS l
            ON l.item_id = u.id 
			   AND l.like_type_id = 2
               OR l.item_id = m.id AND l.like_type_id = 1
               OR l.item_id = t.id AND l.like_type_id = 3
    GROUP BY u.id
    ORDER BY p.birthday DESC
    LIMIT 10
)
SELECT SUM(rate) as overall FROM rate_likes;

-- Т.к. мы работает с id пользователя и его днем рождения, то можно делать выборку сразу из таблицы profiles
WITH rate_likes as (
    SELECT 
        count(l.id) as rate
    FROM profiles AS p
        LEFT JOIN media as m
            ON m.user_id = p.user_id
        LEFT JOIN messages as t
            ON t.from_user_id = p.user_id
        LEFT JOIN likes AS l ON    
                  l.item_id = p.user_id AND l.like_type_id = 2
               OR l.item_id = m.id      AND l.like_type_id = 1
               OR l.item_id = t.id      AND l.like_type_id = 3
    GROUP BY p.user_id
    ORDER BY p.birthday DESC
    LIMIT 10
)
SELECT SUM(rate) as overall FROM rate_likes;
-- Можно добавить индекс на (likes.item_id , likes.like_type_id), что ускорит выборку
CREATE INDEX rate_likes_item_id_like_type_id) ON (item_id, like_type_id);


-- Если это не помогает, тогда имеет смысл денормализовать таблицу лайков.
CREATE TABLE message_likes (
    messages_id INT,
    from_user_id INT,
    PRIMARY KEY (messages_id, from_user_id)
);

CREATE TABLE user_likes (
    to_user_id INT,
    from_user_id INT,
    PRIMARY KEY (to_user_id, from_user_id)
);

CREATE TABLE media_likes (
    media_id INT,
    from_user_id INT,
    PRIMARY KEY (media_id, from_user_id)
);

START TRANSACTION;
INSERT INTO media_likes   (media_id, from_user_id)    SELECT item_id, user_id FROM likes WHERE like_type_id = 1;
INSERT INTO user_likes    (to_user_id, from_user_id)  SELECT item_id, user_id FROM likes WHERE like_type_id = 2;
INSERT INTO message_likes (messages_id, from_user_id) SELECT item_id, user_id FROM likes WHERE like_type_id = 3;

DROP TABLE likes;
DROP TABLE like_types;

COMMIT;