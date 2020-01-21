'''1. Определение количества различных подстрок с использованием хеш-функции.
Пусть на вход функции дана строка.
Требуется вернуть количество различных подстрок в этой строке.
Примечания:
* в сумму не включаем пустую строку и строку целиком;
* без использования функций для вычисления хэша (hash(), sha1() или любой другой из модуля hashlib задача считается не решённой.'''


from hashlib import sha1


def find_substring_count(s: str) -> int:
	assert len(s)>0 , 'Строка не может быть пустой'
	res = set()
	for i in range(0, len(s)-1):
		res.add(sha1(s[0:i].encode('utf-8')).hexdigest())
		for j in range(0,len(s),i+1):
			res.add(sha1(s[i:j].encode('utf-8')).hexdigest())
			for k in range(j,len(s),j+1):
				res.add(sha1(s[k :j].encode('utf-8')).hexdigest())
	return len(res)

print(find_substring_count('baa'))
