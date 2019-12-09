#3. В массиве случайных целых чисел поменять местами минимальный и максимальный элементы.
import random
m = [random.randint(0, 100) for _ in range(10)]
print(m)
max = min = 0
for i in range(len(m)):
	if m[max] < m[i]: max = i
	elif m[min] > m[i]: min = i

tmp = m[min]
m[min] = m[max]
m[max] = tmp
print(m)
