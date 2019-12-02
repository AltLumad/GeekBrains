#3. Сформировать из введенного числа обратное по порядку входящих в него цифр и вывести на экран. 
#Например, если введено число 3486, надо вывести 6843.
n = int(input('Input natural number: '))
reverse = 0
while n != 0:
	reverse *= 10
	reverse += n % 10
	n = n // 10
print(reverse)