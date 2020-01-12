'''2. Отсортируйте по возрастанию методом слияния одномерный вещественный массив,
заданный случайными числами на промежутке [0; 50).
Выведите на экран исходный и отсортированный массивы.'''

import random as r
ARR_SIZE = 25


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    if len(arr) == 2:
        arr[0], arr[1] = arr[1], arr[0]
        return arr
    n = len(arr) // 2
    left = merge_sort(arr[0: n])
    right = merge_sort(arr[n: len(arr)])
    res = []
    l, r = 0, 0
    while l < len(left) or r < len(right):
        if len(left) == l:
            res.append(right[r])
            r += 1
            continue
        if len(right) == r:
            res.append(left[l])
            l += 1
            continue

        if left[l] < right[r]:
            res.append(left[l])
            l += 1
        else:
            res.append(right[r])
            r += 1

    return res


array = [r.randint(0, 50) for _ in range(ARR_SIZE)]

print(array)
array = merge_sort(array)
print(array)
