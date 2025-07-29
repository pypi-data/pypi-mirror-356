def beam_code():
    return """
import heapq

def beam_search(graph, start, goal, heuristic, beam_width):
    open_list = [(heuristic[start], start)]
    visited = {start: None}

    while open_list:
        # Sorting based on heuristic values
        open_list.sort()
        open_list = open_list[:beam_width]  # Keep only top `beam_width` nodes

        next_nodes = []
        for _, current in open_list:
            if current == goal:
                return reconstruct_path(visited, current)

            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited[neighbor] = current
                    heapq.heappush(next_nodes, (heuristic[neighbor], neighbor))  # Using heapq

        open_list = next_nodes  

    return None

def reconstruct_path(visited, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = visited[goal]
    return path[::-1]  

# Graph with weighted edges
graph = {
    'A': [('B'), ('D')],
    'B': [('A'), ('C'), ('E')],
    'C': [('B'), ('F'), ('J')],
    'D': [('A'), ('E'), ('G')],
    'E': [('B'), ('D'), ('F'), ('H')],
    'F': [('C'), ('E'), ('I'), ('J')],
    'G': [('D'), ('H')],
    'H': [('E'), ('G'), ('I')],
    'I': [('H'), ('F')],
    'J': [('C'), ('F')]
}

heuristic = {
    'A': 10, 'B': 7, 'C': 8, 'D': 11, 'E': 6,
    'F': 5, 'G': 33, 'H': 9, 'I': 8, 'J': 0
}



print("Path:", beam_search(graph, 'A', 'J', heuristic, beam_width=1))
import heapq

def beam_search(graph, start, goal, heuristic, beam_width):
    open_list = [(heuristic[start], start)]
    visited = {start: None}

    while open_list:
        # Sorting based on heuristic values
        open_list.sort()
        open_list = open_list[:beam_width]  # Keep only top `beam_width` nodes

        next_nodes = []
        for _, current in open_list:
            if current == goal:
                return reconstruct_path(visited, current)

            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited[neighbor] = current
                    heapq.heappush(next_nodes, (heuristic[neighbor], neighbor))  # Using heapq

        open_list = next_nodes  

    return None

def reconstruct_path(visited, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = visited[goal]
    return path[::-1]  

# Graph with weighted edges
graph = {
    'A': [('B'), ('D')],
    'B': [('A'), ('C'), ('E')],
    'C': [('B'), ('F'), ('J')],
    'D': [('A'), ('E'), ('G')],
    'E': [('B'), ('D'), ('F'), ('H')],
    'F': [('C'), ('E'), ('I'), ('J')],
    'G': [('D'), ('H')],
    'H': [('E'), ('G'), ('I')],
    'I': [('H'), ('F')],
    'J': [('C'), ('F')]
}

heuristic = {
    'A': 10, 'B': 7, 'C': 8, 'D': 11, 'E': 6,
    'F': 5, 'G': 33, 'H': 9, 'I': 8, 'J': 0
}



print("Path:", beam_search(graph, 'A', 'J', heuristic, beam_width=1))


"""