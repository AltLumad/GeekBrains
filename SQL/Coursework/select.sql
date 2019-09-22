/*---------------------------------------------------*/
-- Кто больше всех совершил переводов из пользователей
SELECT U.fullname, COUNT(payment_from)  FROM transactions T
  INNER JOIN account A ON A.id = T.payment_from
  INNER JOIN users U on U.id = A.owner_id
WHERE A.owner_type_id = 1
GROUP BY U.id
