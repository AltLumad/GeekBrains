#4. Определить, какое число в массиве встречается чаще всего.
import random
m = [random.randint(0, 50) for _ in range(30)]
print(m)
d = {}
for i in m:
	if i in d: d[i] += 1
	else: d[i] = 1
print(d)
max = None
for key in d:
	if not max or d[max] < d[key]:
		max = key

print(max)
	
	