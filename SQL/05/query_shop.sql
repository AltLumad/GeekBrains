/*
1)Составьте список пользователей users, 
которые осуществили хотя бы один заказ orders в интернет магазине.
*/
SELECT name FROM users U
WHERE EXISTS(SELECT 1 FROM orders WHERE user_id = U.id);

/*
2)Выведите список товаров products и разделов catalogs, 
который соответствует товару.*/

SELECT  P.name AS product_name
       ,C.name AS catalog_name
FROM products P
INNER JOIN catalogs C on C.id = P.catalog_id;


