import numpy as np
from pathlib import Path
from collections import defaultdict

np.random.seed(44)

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

