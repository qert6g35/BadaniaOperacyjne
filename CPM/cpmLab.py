import numpy as np
from pathlib import Path
from collections import defaultdict

# nazwa pliku bez dopisku .txt
# czasy i krawędzie jako listy
def loadData(filename):
    
    my_file = Path("./"+filename+".txt")
    
    if not my_file.is_file():
        my_file = Path("./CPM/"+filename+".txt")

    f = open(my_file, "r")
    f.readline()

    timesraw = f.readline()
    times = np.fromstring(timesraw,sep=" ").astype(np.int16)
    
    edgesraw = f.readline()
    edgesraw = np.fromstring(edgesraw,sep=" ").astype(np.int16)-1
    edges = edgesraw.reshape((-1,2),order='C')

    # print("times: ", times)
    # print("edges: ", edges)
    return times, edges




def topologicalSortKahn(V,E):
    indegree = defaultdict(int)
    N = [i for i in range(0,len(V))]
    Q = []
    TO = []
    
    for e in E[:,1]:
        indegree[e] += 1

    for n in N:
        if indegree[n] == 0:
            Q.append(n)

    while Q:
        node = Q.pop(0)
        TO.append(node)

        neighbours = []
        for e in E:
            if e[0] == node:
                neighbours.append(e[1])

        for n in neighbours:
            indegree[n] -= 1
            if indegree[n] == 0:
                Q.append(n)


    newV = [V[i] for i in TO]
    newE = np.array([E[i] for i in TO])
    return newV, newE, TO

# V,E = loadData("data10")
# V,E, TO = topologicalSortKahn(V,E)

# print(TO)