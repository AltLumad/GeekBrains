'''1. Проанализировать скорость и сложность одного любого алгоритма из разработанных в рамках домашнего задания первых трех уроков.
Примечание. Идеальным решением будет:
a. выбрать хорошую задачу, которую имеет смысл оценивать,
b. написать 3 варианта кода (один у вас уже есть),
c. проанализировать 3 варианта и выбрать оптимальный,
d. результаты анализа вставить в виде комментариев в файл с кодом (не забудьте указать, для каких N вы проводили замеры),
e. написать общий вывод: какой из трёх вариантов лучше и почему.'''

#Урок 3. Задача4. Определить, какое число в массиве встречается чаще всего.
import random
import cProfile

def On(n):
	random.seed(n)
	m = [random.randint(0, 50) for _ in range(n)]	
	d = {}
	for i in m:
		if i in d: d[i] += 1
		else: d[i] = 1
	max = None
	for key in d:
		if not max or d[max] < d[key]:
			max = key
	return max

def Onlogn(n):
	random.seed(n)
	m = sorted([random.randint(0, 50) for _ in range(n)])
	max = tmp = 0
	prev = res = None
	for i in m:
		if i == prev:
			tmp += 1
		else:
			if max <= tmp: 
				max =  tmp
				res = prev
			tmp, prev = 1, i

	if max <= tmp: 
		max =  tmp
		res = i
	
	return res

def On2(n):
	random.seed(n)
	m = [random.randint(0, 50) for _ in range(n)]
	m_set = set(m)
	quantity_full = 0
	res = None
	for i in m_set:
		quantity = m.count(i)
		if quantity >= quantity_full:
			quantity_full = quantity
			res = i
	return res
	
	
'''
n = 1000
loops = 1000
t1.On:  	best of 5: 2.15 msec per loop
t1.Onlogn: 	best of 5: 2.08 msec per loop
t1.On2:		best of 5: 3.24 msec per loop

n = 10000
loops = 50
t1.On:		best of 5: 19.4 msec per loop
t1.Onlogn: 	best of 5: 20.3 msec per loop
t1.On2: 	best of 5: 32 msec per loop

n = 100000
loops = 10
t1.On:		best of 5: 196 msec per loop
t1.Onlogn:	best of 5: 202 msec per loop
t1.On2:		best of 5: 306 msec per loop


n = 1000000
loops = 1
t1.On:		best of 5: 2.03 sec per loop
t1.On2:		best of 5: 3.15 sec per loop
t1.Onlogn: 	best of 5: 2.12 sec per loop
'''

''' cProfile
   
   On(1000000)
   5255450 function calls in 3.001 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1000000    0.953    0.000    2.044    0.000 random.py:174(randrange)
  1000000    0.381    0.000    2.425    0.000 random.py:218(randint)
  1000000    0.772    0.000    1.091    0.000 random.py:224(_randbelow)
        1    0.000    0.000    0.000    0.000 random.py:97(seed)
        1    0.192    0.192    2.997    2.997 t1.py:13(On)
        1    0.380    0.380    2.805    2.805 t1.py:15(<listcomp>)
        1    0.000    0.000    3.001    3.001 {built-in method builtins.exec}
  1000000    0.098    0.000    0.098    0.000 {method 'bit_length' of 'int' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
  1255442    0.222    0.000    0.222    0.000 {method 'getrandbits' of '_random.Random' objects}


	Onlogn(1000000)
	5255451 function calls in 3.100 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1000000    0.963    0.000    2.070    0.000 random.py:174(randrange)
  1000000    0.385    0.000    2.454    0.000 random.py:218(randint)
  1000000    0.783    0.000    1.106    0.000 random.py:224(_randbelow)
        1    0.000    0.000    0.000    0.000 random.py:97(seed)
        1    0.100    0.100    3.095    3.095 t1.py:26(Onlogn)
        1    0.388    0.388    2.842    2.842 t1.py:28(<listcomp>)
        1    0.000    0.000    3.100    3.100 {built-in method builtins.exec}
        1    0.154    0.154    0.154    0.154 {built-in method builtins.sorted}
  1000000    0.100    0.000    0.100    0.000 {method 'bit_length' of 'int' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
  1255442    0.224    0.000    0.224    0.000 {method 'getrandbits' of '_random.Random' objects}

	
	On2(1000000)
	5255501 function calls in 4.127 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1000000    0.965    0.000    2.078    0.000 random.py:174(randrange)
  1000000    0.388    0.000    2.466    0.000 random.py:218(randint)
  1000000    0.787    0.000    1.113    0.000 random.py:224(_randbelow)
        1    0.000    0.000    0.000    0.000 random.py:97(seed)
        1    0.016    0.016    4.125    4.125 t1.py:46(On2)
        1    0.385    0.385    2.851    2.851 t1.py:48(<listcomp>)
        1    0.000    0.000    4.127    4.127 {built-in method builtins.exec}
  1000000    0.100    0.000    0.100    0.000 {method 'bit_length' of 'int' objects}
       51    1.258    0.025    1.258    0.025 {method 'count' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
  1255442    0.227    0.000    0.227    0.000 {method 'getrandbits' of '_random.Random' objects}
'''

#Самое затратное в этих алгоритмах это создание и инициализация массива функцией randint.
#Однако, видно что с увеличением n, функция On начинает обгонять Onlogn. И обе функции оставляют позади On2
#Сложность функций: On - O(n); Onlogn - O(nlog(n)); On2 - O(n**2); 
#Для n < 1000. Разницы в выборе функции нет.
#Для n < 100000. Или On или Onlogn
#Далее однозначно On
