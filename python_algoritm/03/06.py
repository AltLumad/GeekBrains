#6. В одномерном массиве найти сумму элементов, находящихся между минимальным и максимальным элементами. 
#Сами минимальный и максимальный элементы в сумму не включать.
import random
m = [random.randint(0, 100) for _ in range(15)]
print(m)
max = min = sum = 0
for i in range(len(m)):
	if m[max] < m[i]: max = i
	elif m[min] > m[i]: min = i
begin = max if max < min else min
end = max if max > min else min

for i in range(begin+1, end):
	sum += m[i]
print(sum)