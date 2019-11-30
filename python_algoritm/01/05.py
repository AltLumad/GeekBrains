#5. Пользователь вводит номер буквы в алфавите. Определить, какая это буква.
import string
try:
	n = int(input('Input number a char: '))
	if n < 1 or n > 26: raise Exception()
	print(chr(n+96))
except:
	print("Your char number is invalid")
	