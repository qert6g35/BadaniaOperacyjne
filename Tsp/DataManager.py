import numpy as np
from pathlib import Path
from collections import defaultdict

np.random.seed(44)

def generateData(n,map_size=100):
    G_x = (np.array([np.random.random_integers(0,map_size,n)]*n)).reshape([n,n])
    G_y = (np.array([np.random.random_integers(0,map_size,n)]*n)).reshape([n,n])
    dist_matrix = np.zeros([n,n])
    Gx = G_x - G_x.T
    Gy = G_y - G_y.T
    dist_matrix = Gx*Gx + Gy*Gy
    dist_matrix = dist_matrix
    return dist_matrix


print(generateData(10))



def loadData(filename):
    
    my_file = Path("./"+filename+".txt")
    
    if not my_file.is_file():
        my_file = Path("./MinPath/"+filename+".txt")

    f = open(my_file, "r")
    try:
        count = int(f.readline())
    except:
        return None
    
    line = ""
    for _ in range(0,count):
        line += f.readline()[0:-1]

    Out = np.fromstring(line,sep=" ").astype(np.int16)
    return Out.reshape((-1,count),order='C')