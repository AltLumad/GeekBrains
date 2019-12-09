#5. В массиве найти максимальный отрицательный элемент. Вывести на экран его значение и позицию в массиве.
import random
m = [random.randint(-100, 100) for _ in range(30)]
print(m)
max_negative = 0
for i in range(len(m)):
	if m[i] < 0 and (m[max_negative] < m[i] or m[max_negative] >= 0):
		max_negative = i
	
print(f'max negative element\nposition: {max_negative}\nvalue: {m[max_negative]}')
		