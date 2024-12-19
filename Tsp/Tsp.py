import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as pcolors
# from DataManager import generateDistanceMatrix


def generateCoordinates(n,max_coordinate_value=100):
    cooridnates = np.random.randint(0,max_coordinate_value+1,n*2).reshape([-1,2])
    return cooridnates

def generateDistanceMatrix(n,max_coordinate_value=100):

    coordinates = generateCoordinates(n,max_coordinate_value)

    x_coor = (np.array([coordinates[:,0]]*n)).reshape([n,n])
    y_coor = (np.array([coordinates[:,1]]*n)).reshape([n,n])

    x_dist = x_coor - x_coor.T
    y_dist = y_coor - y_coor.T

    dist_matrix = np.sqrt(np.power(x_dist,2) + np.power(y_dist,2))

    return dist_matrix

def coordinatesToDistMatrix(coordinates):

    n = coordinates.shape[0]

    x_coor = (np.array([coordinates[:,0]]*n)).reshape([n,n])
    y_coor = (np.array([coordinates[:,1]]*n)).reshape([n,n])

    x_dist = x_coor - x_coor.T
    y_dist = y_coor - y_coor.T

    dist_matrix = np.sqrt(np.power(x_dist,2) + np.power(y_dist,2))

    return dist_matrix

def plot_path(nodes, path,dists,titles):
    paths_n = len(path)
    """Plots the given path using matplotlib."""
    fig, axs = plt.subplots(1, paths_n, figsize=(8*paths_n, 8))
    colors = list(pcolors.TABLEAU_COLORS.keys())
    print(colors)
    for j in range(len(path)):
        one_path = path[j]
        color = colors[j]
        for i in range(len(one_path) - 1):
            start = nodes[one_path[i]]
            end = nodes[one_path[i + 1]]
            axs[j].plot([start[0], end[0]], [start[1], end[1]], color=color, alpha=0.7)
    
    # Highlight the nodes
        for i, node in enumerate(nodes):
            axs[j].scatter(node[0], node[1], c='red', zorder=5)
            axs[j].text(node[0] + 0.5, node[1] + 0.5, str(i), fontsize=9, color='darkgreen')

        axs[j].set_title(titles[j]+" - score: "+str(dists[j]))
        axs[j].set_xlabel("X")
        axs[j].set_ylabel("Y")
        axs[j].grid(True)
        axs[j].axis('equal')
    plt.show()




def FI(distance_matrix, start_node=0):
    node_count = len(distance_matrix)
    
    # Step 1: Initialize with the farthest pair
    max_dist = -1
    start_node, farthest_node = 0, 0
    for i in range(node_count):
        for j in range(i + 1, node_count):
            if distance_matrix[i, j] > max_dist:
                max_dist = distance_matrix[i, j]
                start_node, farthest_node = i, j

    path = [start_node, farthest_node, start_node]
    visited = {start_node, farthest_node}
    total_distance = 2 * max_dist

    # Step 2: Iteratively insert the farthest node into the best position
    while len(visited) < node_count:
        # Find the farthest unvisited node from the current path
        farthest_unvisited_node = None
        max_min_dist = -1
        for i in range(node_count):
            if i not in visited:
                min_dist_to_path = min(distance_matrix[i][p] for p in path)
                if min_dist_to_path > max_min_dist:
                    max_min_dist = min_dist_to_path
                    farthest_unvisited_node = i

        # Find the best position to insert the farthest unvisited node
        best_position = 0
        best_increase = float('inf')
        for i in range(len(path) - 1):
            current_node, next_node = path[i], path[i + 1]
            increase = (distance_matrix[current_node, farthest_unvisited_node] +
                        distance_matrix[farthest_unvisited_node, next_node] -
                        distance_matrix[current_node, next_node])
            if increase < best_increase:
                best_increase = increase
                best_position = i + 1

        # Insert the node into the path and update the total distance
        path.insert(best_position, farthest_unvisited_node)
        total_distance += best_increase
        visited.add(farthest_unvisited_node)

    return path, round(total_distance)



def NN(distance_matrix, start_node=0):
    node_count = len(distance_matrix)
    visited = [False] * node_count
    path = [start_node]
    visited[start_node] = True
    total_distance = 0
    
    current_node = start_node
    for _ in range(node_count - 1):
        # Find the nearest unvisited node
        nearest_neighbor = None
        min_distance = float('inf')
        
        for neighbor in range(node_count):
            if not visited[neighbor] and distance_matrix[current_node, neighbor] < min_distance:
                nearest_neighbor = neighbor
                min_distance = distance_matrix[current_node, neighbor]
        
        # Move to the nearest neighbor
        path.append(nearest_neighbor)
        total_distance += min_distance
        visited[nearest_neighbor] = True
        current_node = nearest_neighbor
    
    # Return to the start node to complete the cycle
    total_distance += distance_matrix[current_node, start_node]
    path.append(start_node)
    
    return path, round(total_distance)


# Example usage
coordinates = generateCoordinates(20)
distMatrix = coordinatesToDistMatrix(coordinates)

pathNN, distNN = NN(distMatrix)
pathFI, distFI = FI(distMatrix)

print("FI Path:", pathNN, ", distance: ", distNN)
print("NN Path:", pathFI, ", distance: ", distFI)

plot_path(coordinates,[pathFI,pathNN],[distFI,distNN],["FI","NN"]) ## tak na szybko :)