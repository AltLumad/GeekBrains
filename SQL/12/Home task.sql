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

/*
2)
(по желанию) Попытаться улучшить результат оптимизации примера, 
который рассмотрен на занятии*/