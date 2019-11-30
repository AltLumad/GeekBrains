#	По длинам трех отрезков, введенных пользователем, определить возможность существования треугольника, составленного из этих отрезков. 
#Если такой треугольник существует, то определить, является ли он разносторонним, равнобедренным или равносторонним.

a, b, c = map(int, input('Input a,b,c: ').split())
if min(a,b,c) < 1:
	print('triangle is not exist')
elif a == b and b == c and a == c:
	print('equilateral triangle')
elif a == b or b == c or c == a:
	print('isosceles  triangle')
elif (a < b + c) and (b < a + c) and (c < a + b):
	print('versatile triangle')
else:
	print('triangle is not exist')