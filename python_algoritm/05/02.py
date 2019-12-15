'''
Написать программу сложения и умножения двух шестнадцатеричных чисел. 
При этом каждое число представляется как массив, элементы которого это цифры числа.
Например, пользователь ввёл A2 и C4F. 
Сохранить их как [‘A’, ‘2’] и [‘C’, ‘4’, ‘F’] соответственно. 
Сумма чисел из примера: [‘C’, ‘F’, ‘1’].
Произведение - [‘7’, ‘C’, ‘9’, ‘F’, ‘E’].
'''

from collections import namedtuple

lst = input('Enter two HEX-number: ').split()
HEXKeeper = namedtuple('HEXKeeper','left right')

hexs = HEXKeeper(list(lst[0]), list(lst[1]))
left = int(''.join(hexs.left), 16)
right = int(''.join(hexs.right), 16)

hsum = hex(left + right)
hmultiply = hex(left * right)
res = HEXKeeper(list(str(hsum))[2:], list(str(hmultiply))[2:])
print(f"First op: \t{hexs.left}")
print(f"Second op: \t{hexs.right}")
print(f"Summa: \t\t{res.left}")
print(f"Multiply: \t{res.right}")

