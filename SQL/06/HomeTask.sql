-- 2)Пусть задан некоторый пользователь.
-- Из всех друзей этого пользователя найдите человека, который больше всех общался с нашим пользоваетелем.
SELECT (SELECT fullname from users WHERE id = best_friend_id) AS best_fiend,
        MAX(count_messages) as count_messages 
FROM (
SELECT best_friend_id, COUNT(*) AS count_messages FROM (
	SELECT to_user_id AS best_friend_id FROM messages WHERE from_user_id = 1
	union ALL
	SELECT from_user_id  FROM messages WHERE to_user_id = 1
) AS T
GROUP BY best_friend_id
) AS FD -- FRIEND_STATISTIC
GROUP BY best_fiend
ORDER BY  count_messages DESC
LIMIT 1;

-- 3) Подсчитать общее количество лайков, которые получили 10 самых молодых пользователей.

SELECT COUNT(user_id) FROM (
	SELECT user_id, (SELECT birthday 
                     FROM profiles as P 
					 WHERE P.user_id = L.user_id) as birthday
	FROM likes as L
    ORDER BY birthday DESC 
    LIMIT 10
) AS T;

-- 4) Определить кто больше поставил лайков (всего) - мужчины или женщины?

SELECT sex FROM (
SELECT sex, COUNT((SELECT COUNT(*) FROM likes as L where L.user_id = P.user_id)) as gender_likes_count FROM profiles as P
WHERE sex = 'm'
GROUP BY sex
UNION ALL
SELECT sex, COUNT((SELECT COUNT(*) FROM likes as L where L.user_id = P.user_id)) FROM profiles as P
WHERE sex = 'f'
GROUP BY sex
) AS T
GROUP BY sex
ORDER BY MAX(gender_likes_count) DESC
LIMIT 1;


-- 5) Найти 10 пользователей, которые проявляют наименьшую активность в использовании социальной сети.
SELECT (SELECT fullname FROM users where id = user_id) fullname,  SUM(T.rnk) AS rnk
FROM(
	SELECT from_user_id as user_id, COUNT(*) as rnk  FROM messages -- Неактивные пользователи мало отправляют сообщения
	GROUP BY from_user_id
	UNION ALL
	SELECT user_id, COUNT(*)  FROM likes -- Неактивные пользователи мало лайкуют
	GROUP BY user_id
	UNION ALL
	SELECT user_id, COUNT(*)  FROM friendship -- И друзей у таких пользователей мало
	GROUP BY user_id
	UNION ALL
	SELECT friend_id, COUNT(*)  FROM friendship 
	GROUP BY friend_id
	UNION ALL
	SELECT user_id, COUNT(*)  FROM communities_users
	GROUP BY user_id
) AS T
GROUP BY fullname
ORDER BY rnk
LIMIT 10;











