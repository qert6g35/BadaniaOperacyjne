import random

def generate_random_max_flow_instance(n):
    # Create an n x n matrix initialized with 0s
    capacity_matrix = [[0] * n for _ in range(n)]
    
    # Randomly assign capacities between nodes
    for i in range(n):
        for j in range(n):
            if i != j:  # No self-loops
                capacity_matrix[i][j] = random.randint(0, 50)  # Random capacity between 0 and 10
    
    for i in range(1, n-1):
        if capacity_matrix[0][i] == 0 and random.uniform(0,1) < 0.125:  # If no direct connection, create one
            capacity_matrix[0][i] = random.randint(1, 50)
        if capacity_matrix[i][n-1] == 0 and random.uniform(0,1) < 0.125:  # If no direct connection to sink, create one
            capacity_matrix[i][n-1] = random.randint(1, 50)

    return capacity_matrix

