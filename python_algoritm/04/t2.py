'''
2. Написать два алгоритма нахождения i-го по счёту простого числа. 
Функция нахождения простого числа должна принимать на вход натуральное и возвращать соответствующее простое число. 
Проанализировать скорость и сложность алгоритмов.
Первый — с помощью алгоритма «Решето Эратосфена».
Второй — без использования «Решета Эратосфена».
'''
import cProfile
def sieve(n):
	a = [i for i in range(n**2)]
	for i in range(2,n**2):
		if a[i] == 0: continue
		for j in range(2*i,n**2,i):
			a[j] = 0
	t = [i for i in a if i != 0] 
	return t[n]

def prime(n):
	if n == 1:
		return 2
	a = [i for i in range(n**2)]
	res = []
	for i in range(2, n**2):
		cnt = 0
		for j in range(2,i):
			if i % j == 0:
				cnt += 1
		if cnt == 0:
			res.append(i)
			if len(res) == n:
				break
	return res.pop()


''' timeit
n = 100 
loops = 100
t2.sieve
best of 5: 5.24 msec per loop

n = 100 
loops = 100
t2.prime
best of 5: 13.9 msec per loop	
'''


'''
cProfile.run('sieve(1000)')
         6 function calls in 0.680 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.014    0.014    0.680    0.680 <string>:1(<module>)
        1    0.103    0.103    0.103    0.103 t2.py:10(<listcomp>)
        1    0.046    0.046    0.046    0.046 t2.py:15(<listcomp>)
        1    0.517    0.517    0.666    0.666 t2.py:9(sieve)
        1    0.000    0.000    0.680    0.680 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

cProfile.run('prime(1000)')
         2006 function calls in 3.577 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.017    0.017    3.577    3.577 <string>:1(<module>)
        1    3.466    3.466    3.560    3.560 t2.py:18(prime)
        1    0.093    0.093    0.093    0.093 t2.py:21(<listcomp>)
        1    0.000    0.000    3.577    3.577 {built-in method builtins.exec}
     1000    0.000    0.000    0.000    0.000 {built-in method builtins.len}
     1000    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 {method 'pop' of 'list' objects}
'''

#Такая разница во времени получается из-за того что сложность функции sieve O(n**2), в то время как prime O(n**4)
