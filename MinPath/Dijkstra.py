import heapq
from DataManagment import loadData

def matrix_to_graph(matrix):
    graph = {}
    num_vertices = len(matrix)
    for i in range(num_vertices):
        graph[i] = {}
        for j in range(num_vertices):
            if matrix[i][j] != float('infinity') and matrix[i][j] != 0:
                graph[i][j] = matrix[i][j]
    return graph

def dijkstra(graph, source):
   
    dist = {vertex: float('infinity') for vertex in graph}
    prev = {vertex: None for vertex in graph}
    dist[source] = 0
    
    Q = [(0, source)]

    while Q:
        current_distance, current_vertex = heapq.heappop(Q)

        for neighbor, v in graph[current_vertex].items():
            alt = current_distance + v
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = current_vertex
                heapq.heappush(Q, (alt, neighbor))

    return dist, prev


print(dijkstra(matrix_to_graph(loadData("MData5")),0))