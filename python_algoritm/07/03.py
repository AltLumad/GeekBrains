'''3. Массив размером 2m + 1, где m — натуральное число, заполнен случайным образом.
Найдите в массиве медиану.
Медианой называется элемент ряда, делящий его на две равные части:
    в одной находятся элементы, которые не меньше медианы, в другой — не больше медианы.
Примечание: задачу можно решить без сортировки исходного массива.
Но если это слишком сложно, используйте метод сортировки,
который не рассматривался на уроках (сортировка слиянием также недопустима).'''


import random as r
m = 12
ARR_SIZE = 2*m + 1



def get_median(array):
    arr = array.copy()
    while len(arr) > 1:
        idx_min, idx_max = 0, 0
        for i in range(len(arr)):
            if arr[idx_min] > arr[i]:
                idx_min = i
            if arr[idx_max] < arr[i]:
                idx_max = i
        if idx_min > idx_max:
            arr.pop(idx_min)
            arr.pop(idx_max)
        else:
            arr.pop(idx_max)
            arr.pop(idx_min)
    return arr[0]


array = [r.randint(0, 50) for _ in range(ARR_SIZE)]
print(array)
print(get_median(array))
