# nazwa pliku bez dopisku .txt
# czasy i krawędzie jako listy
def loadData(filename):
    f = open(filename+".txt", "r")
    f.readline()
    timesraw = f.readline()[:-1]
    timesraw = timesraw.split(" ")
    times = [int(timesraw[i]) for i in range(0,len(timesraw))]
    
    edgesraw = f.readline()[:-1]
    edgesraw = edgesraw.split("  ")
    edgesraw = [edgesraw[i].split(" ") for i in range(0,len(edgesraw))]
    edges = []
    for j in range(0,len(edgesraw)):
        edges.append([int(edgesraw[j][i]) for i in range(0,len(edgesraw[j]))])

    print("times: ", times)
    print("edges: ", edges)
    return times, edges


loadData("data10")
