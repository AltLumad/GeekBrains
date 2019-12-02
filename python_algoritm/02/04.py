#4. Найти сумму n элементов следующего ряда чисел: 1, -0.5, 0.25, -0.125,… Количество элементов (n) вводится с клавиатуры.
n = int(input('Input natural number: '))
k, sum = 1., 0.
for i in range(n):
	sum += k
	k /= -2
print(sum)
