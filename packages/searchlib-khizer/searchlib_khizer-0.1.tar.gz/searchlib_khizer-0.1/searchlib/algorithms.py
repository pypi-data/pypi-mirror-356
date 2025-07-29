def astar_code():
    return """
import heapq

graph = {
    'S': [('A', 3), ('B', 2)],
    'A': [('C', 4), ('D', 1)],
    'B': [('E', 3), ('F', 1)],
    'C': [], 'D': [], 'E': [('H', 5)], 'F': [('I', 2), ('G', 3)],
    'H': [], 'I': [], 'G': []
}

heuristics = {
    'S': 12, 'A': 12, 'B': 4, 'C': 7, 'D': 3, 'E': 8, 'F': 2,
    'H': 9, 'I': 13, 'G': 0
}

def a_star_search(start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristics[start], 0, [start]))

    while open_list:
        f, g, path = heapq.heappop(open_list)
        current = path[-1]

        if current == goal:
            return path, g

        for neighbor, cost in graph[current]:
            g_new = g + cost
            f_new = g_new + heuristics[neighbor]
            heapq.heappush(open_list, (f_new, g_new, path + [neighbor]))

    return None, float('inf')
"""