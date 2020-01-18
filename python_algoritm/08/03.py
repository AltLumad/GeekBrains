'''3. Написать программу, которая обходит не взвешенный ориентированный граф без петель,
в котором все вершины связаны, по алгоритму поиска в глубину (Depth-First Search).'''

gr = {
    '0': ['2', '3', '4'],
    '1': ['2', '3', '6'],
    '2': ['1', '4', '6'],
    '3': [],
    '4': ['5'],
    '5': ['6'],
    '6': ['4', '5'],
    '7': ['5', '6']
}

def dfs(graph,start, is_visited):
    if start not in is_visited:
        is_visited.append(start)
        for n in graph[start]:
            dfs(graph, n,is_visited)

is_visited = []
dfs(gr, '0', is_visited)
print(is_visited)