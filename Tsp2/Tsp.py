from pathlib import Path
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as pcolors
# from DataManager import generateDistanceMatrix

def read_tsp_instance(file_path):
    coordinates = []
    my_file = Path("./"+file_path)
    
    if not my_file.is_file():
        my_file = Path("./Tsp/"+file_path)

    # Otwieramy plik
    with open(my_file, 'r') as file:
        for line in file:
            # Rozdzielamy dane według białych znaków
            parts = line.split()

            # Konwertujemy odpowiednie dane do formatu float (szerokość, długość)
            id_ = int(parts[0])  # Numer wierzchołka (id)
            x = float(parts[1])  # Szerokość geograficzna
            y = float(parts[2])  # Długość geograficzna
            coordinates.append([x, y])  # Dodajemy współrzędne jako krotkę (x, y)
    
    return coordinates

def loadDistanceMatrix(file_path):

    coordinates = read_tsp_instance(file_path)
    coordinates = np.array(coordinates).reshape([-1,2])
    n = len(coordinates)
    x_coor = (np.array([coordinates[:,0]]*n)).reshape([n,n])
    y_coor = (np.array([coordinates[:,1]]*n)).reshape([n,n])

    x_dist = x_coor - x_coor.T
    y_dist = y_coor - y_coor.T

    dist_matrix = np.sqrt(np.power(x_dist,2) + np.power(y_dist,2))

    return dist_matrix



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
    # print(colors)
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


def RandomPermutation(distance_matrix, start_node=0):
    node_count = len(distance_matrix)
    total_distance = 0
    pi = [i for i in range(1,node_count)]
    random.shuffle(pi)
    pi = [0] + pi + [0]
    prev = 0
    for i in pi:
        total_distance += distance_matrix[prev, i]
        prev = i
    return pi, round(total_distance)


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



# def swap(permutation,V):
#     V.sort()
#     reorder = [i for i in range(0,len(permutation))]
#     reorder = reorder[:V[0]]+reorder[V[0]:V[1]+1][::-1]+reorder[V[1]+1:]
#     #print(reorder)
#     new_permutation = [permutation[i] for i in reorder]
#     return new_permutation

def swap(permutation, v):
    new_permutation = permutation[:]
    new_permutation[v[0]], new_permutation[v[1]] = new_permutation[v[1]], new_permutation[v[0]]
    return new_permutation

def check(distance_matrix,pi,V):
    return (distance_matrix[pi[V[0]]][pi[V[0]+1]] + distance_matrix[pi[V[1]]][pi[V[1]+1]]) - (distance_matrix[pi[V[0]]][pi[V[1]]] + distance_matrix[pi[V[0]+1]][pi[V[1]+1]])

# def twoOpt(dist_matrix,pi,iter):
#     permutation = pi
#     for i in range(iter):
#         V = [random.randint(1,len(pi)-2),random.randint(1,len(pi)-2)]
#         afterSwap = check(dist_matrix,permutation,V)
#         if afterSwap < 0:
#             permutation = swap(permutation,V)
#     return permutation

def f_celu(dist_matrix,permutation):
    total_distance = 0
    permutation = permutation + [permutation[0]]
    prev = permutation[0]
    for i in permutation[1:]:
        total_distance += dist_matrix[prev, i]
        prev = i

    return total_distance

def changeTemp(temp, cooling_rate=0.995,min_temp=1e-5):
    if(temp > min_temp):
        return temp*cooling_rate
    else:
        return -1

def acceptWorse(temp,valuechange):
    return random.uniform(0,1) < math.exp(-valuechange/temp)


def SA(dist_matrx,_permutation = None,_temp=1000, cooling_rate=0.995,L = 10, min_temp=1e-5):
    if _permutation == None:
        permutation = [i for i in range(0,len(dist_matrx))]
    else:
        if _permutation[0] == _permutation[-1]:
            permutation = _permutation[:-1]
        else:
            permutation = _permutation
    temp = _temp
    permutation_values=[f_celu(dist_matrix=dist_matrx,permutation=permutation)]
    v = [0,0]
    permutations = [permutation]
    iters = L
    
    while(temp > 0):
        for i in range(iters):
            candidates = permutation.copy()
            candidates.pop(0)
            v[0] = random.choice(candidates)
            candidates.remove(v[0])       
            v[1] = random.choice(candidates)

            new_perm = swap(permutation,v)
            new_perm_value = f_celu(dist_matrix=dist_matrx,permutation=new_perm)

            if new_perm_value < permutation_values[-1]:
                permutations.append(new_perm)
                permutation_values.append(new_perm_value)
            else:
                if acceptWorse(temp,new_perm_value-permutation_values[-1]):
                    permutations.append(new_perm)
                    permutation_values.append(new_perm_value)
        temp = changeTemp(temp, cooling_rate, min_temp)

    total_distance = min(permutation_values)
    pi_id = permutation_values.index(total_distance)
    permutation = permutations[pi_id]
    permutation = permutation + [permutation[0]]

    return permutation,round(total_distance)

def tabuSearch(dist_matrix, _permutation = None, tabu_size = 10, max_iter = 1000):
    def get_neighbors(permutation):
        neighbors = []
        moves = []
        for i in range(len(permutation)):
            for j in range(i + 1, len(permutation)):
                neighbor = permutation.copy()
                neighbor = neighbor[:i] + neighbor[i:j+1][::-1] + neighbor[j+1:]
                neighbors.append(neighbor)
                moves.append(str(i)+str(j))
        return neighbors, moves

    def f_celu(dist_matrix, permutation):
        return sum(dist_matrix[permutation[i-1]][permutation[i]] for i in range(len(permutation)))

    if _permutation is None:
        permutation = [i for i in range(len(dist_matrix))]
        random.shuffle(permutation)
    else:
        permutation = _permutation

    best_permutation = permutation
    best_cost = f_celu(dist_matrix, permutation)
    tabu_list = []
    
    for _ in range(max_iter):
        neighbors, moves = get_neighbors(permutation)
        new_neighbors = []
        new_moves = []
        for i in range(0,len(neighbors)):
            if moves[i] not in tabu_list and reversed(moves[i]) not in tabu_list:
                new_neighbors.append(neighbors[i])
                new_moves.append(moves[i])
        neighbors = new_neighbors
        moves = new_moves

        if not neighbors:
            break
        
        costs = [f_celu(dist_matrix, n) for n in neighbors]
        min_cost = min(costs)
        id_move = costs.index(min_cost)

        best_neighbor = neighbors[id_move]
        move = moves[id_move]
        
        if min_cost < best_cost:
            best_cost = min_cost
            best_permutation = best_neighbor
        
        permutation = best_neighbor
        tabu_list.append(move)
        
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
    
    return best_permutation, best_cost

def twoOpt(dist_matrix,  _permutation = None):
    def f_celu(dist_matrix, permutation):
        return sum(dist_matrix[permutation[i-1]][permutation[i]] for i in range(len(permutation)))

    def get_neighbors(permutation):
        neighbors = []
        for i in range(len(permutation)):
            for j in range(i + 1, len(permutation)):
                neighbor = permutation.copy()
                neighbor = neighbor[:i] + neighbor[i:j+1][::-1] + neighbor[j+1:]
                neighbors.append(neighbor)
        return neighbors


    if _permutation is None:
        permutation = [i for i in range(len(dist_matrix))]
        random.shuffle(permutation)
    else:
        permutation = _permutation

    best_permutation = permutation
    best_cost = f_celu(dist_matrix, best_permutation)
    
    while True:
        neighbors = get_neighbors(best_permutation)
        costs = [f_celu(dist_matrix, n) for n in neighbors]
        min_cost = min(costs)
        id = costs.index(min_cost)
        if min_cost < best_cost:
            best_permutation = neighbors[id]
            best_cost = min_cost
        else:
            break
    return best_permutation, best_cost

coordinates = generateCoordinates(40)
distMatrix = coordinatesToDistMatrix(coordinates)

print(tabuSearch(distMatrix.copy()))

print(twoOpt(distMatrix.copy()))
# pathNN, distNN = NN(distMatrix)
# pathFI, distFI = RandomPermutation(distMatrix)

# 
# print(pathFI)
# pre_prepare  = pathFI[:-1]
# print(pre_prepare)
# print("start SA for FI permutation")
# saF_permutation, Fpermutation_value_history = SA(distMatrix,pathFI[:-1])
# print("start SA for NN permutation")
# saN_permutation, Npermutation_value_history = SA(distMatrix,pathNN[:-1])
# saN_permutation, Npermutation_value_history = SA(distMatrix)
f_celu(dist_matrix=distMatrix,permutation=[0,1,2,3,4,5,6,7,8,9])
# newPathNN = twoOpt(distMatrix,pathNN,1)

# print("FI Path:", pathNN, ", distance: ", distNN)
# print("NN Path:", pathFI, ", distance: ", distFI)
# print("saF_permutation:",saF_permutation)
# print("saN_permutation:",saN_permutation)
# plot_path(coordinates,[pathFI,saF_permutation,pathNN,saN_permutation],[distFI,Fpermutation_value_history,distNN,Npermutation_value_history],["FI","FI+SA","NN","NN+SA"]) ## tak na szybko :)
# plot_path(coordinates,[pathNN,newPathNN],[distNN,distNN],["NN","NN2opt"]) ## tak na szybko :)