'''1. На улице встретились N друзей. Каждый пожал руку всем остальным друзьям (по одному разу).
Сколько рукопожатий было?

Примечание. Решите задачу при помощи построения графа.
'''
N = int(input('Введите количество друзей: '))
graph = []
res = 0
for i in range(N):
    graph.append([])
    for j in range(N):
        graph[i].append(1 if i != j else 0)
        res += graph[i][j]
    print(graph[i])
res /= 2
print('Всего рукопожатий: ', int(res))

