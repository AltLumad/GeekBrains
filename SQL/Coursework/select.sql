/*---------------------------------------------------*/
-- Кто больше всех совершил переводов из пользователей
SELECT U.fullname, COUNT(payment_from) AS rate  FROM transactions T
  INNER JOIN accounts A ON A.id = T.payment_from
  INNER JOIN users U on U.id = A.owner_id
WHERE A.owner_type_id = 1
GROUP BY U.id
ORDER BY rate DESC
LIMIT 1;

/*----Выписка по всем счетам пользователя за текущий год*/
SELECT A.Name as account, T.opdate , T.Ammount, A.code  FROM transactions T
  INNER JOIN accounts A ON A.id = T.payment_from
  INNER JOIN users U on U.id = A.owner_id
Where A.owner_type_id = 1 
  AND U.id = 2 
  AND YEAR(opdate) = YEAR(NOW())
ORDER BY A.Name, opdate;
