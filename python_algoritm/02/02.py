#2. Посчитать четные и нечетные цифры введенного натурального числа. 
#Например, если введено число 34560, в нем 3 четные цифры (4, 6 и 0) и 2 нечетные (3 и 5).
n = int(input('Input natural number: '))
odd, even = 0, 0
while n != 0:
	if n % 2 == 0:
		even += 1
	else:
		odd += 1
	n = n // 10

print(f'odd: {odd}\neven: {even}')