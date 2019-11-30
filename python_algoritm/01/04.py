#4. Пользователь вводит две буквы. Определить, на каких местах алфавита они стоят, и сколько между ними находится букв.
import string
a,b = input("input ASKII chars: ").split()
apos = string.ascii_letters.find(a)
bpos = string.ascii_letters.find(b)
print(bpos - apos - 1)