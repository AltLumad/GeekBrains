#8. Вводятся три разных числа. 
#Найти, какое из них является средним (больше одного, но меньше другого).

a, b, c = map(int, input('Input a,b,c: ').split())
res = a + b + c - min(a,b,c) - max(a,b,c)
print(res)