'''3. Написать программу, которая обходит не взвешенный ориентированный граф без петель,
в котором все вершины связаны, по алгоритму поиска в глубину (Depth-First Search).
Примечания:
a. граф должен храниться в виде списка смежности;
b. генерация графа выполняется в отдельной функции, которая принимает на вход число вершин.
'''

import random as r
def GraphGenerate(N):
    graph = {}
    for i in range(N):
        graph[i] = []
        for j in range(N):
            if r.randint(1, 4) % 3 == 0:
                graph[i].append(j)

    return graph

def dfs(graph,start, is_visited):
    if start not in is_visited:
        is_visited.append(start)
        for n in graph[start]:
            dfs(graph, n,is_visited)

gr = GraphGenerate(10)
for key, value in gr.items():
    print(key, value)

is_visited = []
dfs(gr, 2, is_visited)
print(is_visited)