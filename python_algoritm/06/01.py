'''
1. Подсчитать, сколько было выделено памяти под переменные в ранее разработанных программах в рамках первых трех уроков. 
Проанализировать результат и определить программы с наиболее эффективным использованием памяти.
Примечание: По аналогии с эмпирической оценкой алгоритмов идеальным решением будет:
a. выбрать хорошую задачу, которую имеет смысл оценивать по памяти;
b. написать 3 варианта кода (один у вас уже есть);
проанализировать 3 варианта и выбрать оптимальный;

c. результаты анализа (количество занятой памяти в вашей среде разработки) вставить в виде комментариев в файл с кодом. Не забудьте указать версию и разрядность вашей ОС и интерпретатора Python;
d. написать общий вывод: какой из трёх вариантов лучше и почему.
Надеемся, что вы не испортили программы, добавив в них множество sys.getsizeof после каждой переменной, а проявили творчество, фантазию и создали универсальный код для замера памяти.
Нажмите, чтобы загрузить файл
'''


#Урок 5. Задание 1. Пользователь вводит данные о количестве предприятий, их наименования и прибыль за четыре квартала для каждого предприятия. 
#Программа должна определить среднюю прибыль (за год для всех предприятий) и отдельно вывести наименования предприятий, чья прибыль выше среднего и ниже среднего.

''' Т.к. количество предприятий заранее неизвестно, то в любом случае придется использовать коллекции. 
Поэтому задача сводится к тому, какую коллекцию оптимально использовать с точки зрения памяти'''

from collections import OrderedDict, deque
import sys

def GetCountOfFactories(): 
	return int(input('Enter the number of factories: '))

def GetFactoriesData(n):
	for i in range(n):
		name = input('Enter the name of the factory: ')
		income = input('Enter the income for the four quarters: ').split()
		income = list(map(int,income))
		avgf = sum(income)/len(income)
		yield (name, avgf)

def PrintResult(avgf, SomeCollection):
	more_avg = True
	print('More than the average')
	for k,v in SomeCollection:
		if v < avgf:
			if more_avg:
				more_avg = False
				print('*'*50)			
				print('Less than the average')			
		print(k)


def PrintSizeOf(items):
	allsize = 0
	for i in items:
		allsize += sys.getsizeof(i)
	print(allsize)

#Через OrderedDict
def WithOrderedDict():
	sumf, n = 0, GetCountOfFactories()
	d = {}
	for name, avgf in GetFactoriesData(n):
		sumf += avgf
		d[name] = avgf
	sumf /= n
	FactoryProfit = OrderedDict(sorted(d.items(),  key = lambda t: t[1]))
	PrintResult(sumf, reversed(FactoryProfit.items()))
	PrintSizeOf([sumf,n, d, FactoryProfit])
#Через List
def WithList():
	sumf, n = 0, GetCountOfFactories()
	lst = []
	for name, avgf in GetFactoriesData(n):
		lst.append((name, avgf))
		sumf += avgf
	sumf /= n
	sorted(lst,  key = lambda t: t[1])
	PrintResult(sumf, reversed(lst))
	PrintSizeOf([sumf,n,lst])
	
#Через deque
def WithDeque():
	sumf, n = 0, GetCountOfFactories()
	d = deque()
	for name, avgf in GetFactoriesData(n):
		d.append((name, avgf))
		sumf += avgf
	sumf /= n
	sorted(d,  key = lambda t: t[1])
	PrintResult(sumf, reversed(d))
	PrintSizeOf([sumf,n, d])


#Версия интерпретатора: 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
#Версия платформы: win32
# Функция				Память(байт)
# WithOrderedDict 		788
# WithList 				148
# WithDeque 			684

#Итого: Обычный List занимает меньше всего места в памяти. 


