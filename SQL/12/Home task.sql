/*
1)
Проверить, исправить при необходимости и оптимизировать следующий запрос:
SELECT CONCAT(u.firstname, ' ', u.lastname) AS user, 
COUNT(l.id) + COUNT(m.id) + COUNT(t.id) AS overall_activity
FROM users AS u
LEFT JOIN
likes AS l
ON l.user_id = u.id
LEFT JOIN
media AS m
ON m.user_id = u.id
LEFT JOIN
messages AS t
ON t.from_user_id = u.id
GROUP BY u.id
ORDER BY overall_activity
LIMIT 10;*/

-- В запросе указана не полная активность пользователя, нет групп
SELECT 
CONCAT(u.firstname, ' ', u.lastname) AS user, 
COUNT(l.id) + COUNT(m.id) + COUNT(t.id) AS overall_activity
FROM users AS u
LEFT JOIN likes AS l
    ON l.user_id = u.id
LEFT JOIN media AS m
    ON m.user_id = u.id
LEFT JOIN messages AS t
    ON t.from_user_id = u.id
LEFT JOIN messages AS t
    ON t.from_user_id = u.id
GROUP BY u.id
ORDER BY overall_activity
LIMIT 10;

/*После разных опытов и анализов, итоговый запрос кардинально поменялся. Помимо увеличения скорости выполнения, исправлены ошибки дублирования строк*/
CREATE INDEX communities_users_user_id_idx ON communities_users(user_id);
CREATE INDEX likes_user_id_idx ON likes(user_id);
CREATE INDEX messages_from_user_id_idx ON messages(from_user_id);
CREATE INDEX media_user_id_idx ON media(user_id);
-- explain
WITH A as (
Select user_id from communities_users
union all 
Select user_id from likes
union all
select from_user_id from messages
union all 
select user_id from media
)
select CONCAT(u.firstname, ' ', u.lastname) AS user, 
	count(*) as overall_activity from A 
inner join users u on u.id = A.user_id
group by user_id 
order by overall_activity
LIMIT 10;


/*
2)
(по желанию) Попытаться улучшить результат оптимизации примера, 
который рассмотрен на занятии*/
