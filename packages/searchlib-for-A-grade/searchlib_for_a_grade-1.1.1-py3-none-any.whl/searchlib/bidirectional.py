def bidirectional_code():
    return """
from collections import deque

def bidirectional_search(graph, start, goal):
    forward_queue = deque([start])
    backward_queue = deque([goal])

    forward_visited = {start: None}
    backward_visited = {goal: None}

    while forward_queue and backward_queue:
        
        if forward_queue:
            current = forward_queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in forward_visited:
                    forward_visited[neighbor] = current
                    forward_queue.append(neighbor)
                    if neighbor in backward_visited:
                        return reconstruct_path(forward_visited, backward_visited, neighbor)

        
        if backward_queue:
            current = backward_queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in backward_visited:
                    backward_visited[neighbor] = current
                    backward_queue.append(neighbor)
                    if neighbor in forward_visited:
                        return reconstruct_path(forward_visited, backward_visited, neighbor)

    return None  

def reconstruct_path(f_visited, b_visited, meeting_point):
    path = []
    node = meeting_point
    while node is not None:
        path.append(node)
        node = f_visited[node]
    path.reverse()
    node = b_visited[meeting_point]
    while node is not None:
        path.append(node)
        node = b_visited[node]
    return path

graph = {
    'A': ['E'],
    'B': ['E'],
    'C': ['F'],
    'D': ['F'],
    'E': ['A', 'B', 'G'],
    'F': ['C', 'D', 'G'],
    'G': ['E', 'F', 'H'],
    'H': ['G', 'I'],
    'I': ['H', 'J', 'K'],
    'J': ['I', 'L', 'M'],
    'K': ['I', 'O'],
    'L': ['J'],
    'M': ['J', 'N'],
    'N': ['M'],
    'O': ['K']
}



print("Path:", bidirectional_search(graph, 'A', 'O'))

"""