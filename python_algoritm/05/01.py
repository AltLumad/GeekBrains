#1. Пользователь вводит данные о количестве предприятий, их наименования и прибыль за четыре квартала для каждого предприятия. 
#Программа должна определить среднюю прибыль (за год для всех предприятий) и отдельно вывести наименования предприятий, чья прибыль выше среднего и ниже среднего.

from collections import OrderedDict
 
d = {}
n = int(input('Enter the number of factories: '))
sumf = 0
for i in range(n):
	name = input('Enter the name of the factory: ')
	income = input('Enter the income for the four quarters: ').split()
	income = list(map(int,income))
	tmp = sum(income)/len(income)
	sumf += tmp
	d[name] = tmp
	print()

avgf = sumf / n
more_avg = True
FactoryProfit = OrderedDict(sorted(d.items(),  key = lambda t: t[1]))
print('More than the average')
for k,v in reversed(FactoryProfit.items()):
	if v < avgf:
		if more_avg:
			more_avg = False
			print('*'*50)			
			print('Less than the average')			
	print(k)		