import numpy as np
from pathlib import Path
from collections import defaultdict

def loadData(filename):
    
    my_file = Path("./"+filename+".txt")
    
    if not my_file.is_file():
        my_file = Path("./MaxFlow/"+filename+".txt")

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