'''1. Отсортируйте по убыванию методом пузырька одномерный целочисленный массив,
заданный случайными числами на промежутке [-100; 100).
Выведите на экран исходный и отсортированный массивы.
Примечания:
a. алгоритм сортировки должен быть в виде функции, которая принимает на вход массив данных,
b. постарайтесь сделать алгоритм умнее, но помните, что у вас должна остаться сортировка пузырьком.
Улучшенные версии сортировки, например, расчёской, шейкерная и другие в зачёт не идут.'''

import random as r
ARR_SIZE = 25


def bubble_sort(arr):
    need_swap = False
    for i in range(ARR_SIZE):
        for j in range(ARR_SIZE - i - 1):
            if arr[j] < arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        need_swap = True
        if not need_swap:
            break

array = [r.randint(-100, 100) for _ in range(ARR_SIZE)]

print(array)
bubble_sort(array)
print(array)

