import numpy as np
from pathlib import Path
from pertTools import loadData, topologicalSortKahn
import scipy.stats as st

def dystrybuantaODWR(X,t,sig):
    return st.norm.ppf(q=X/100,loc=t,scale=sig)

def dystrybuanta(X,t,sig):
    return st.norm.cdf((X - t)/sig)*100

def runPERTfor(filename):
    V_data,E = loadData(filename)
    Vt = [ (v[0] + v[1]*4 + v[2])/6 for v in V_data]
    Vsig = [ np.power((-v[0] + v[2])/6,2) for v in V_data]
    # print(Vt)
    # print(Vsig)
    TO = topologicalSortKahn(Vt,E)
    ES,EF,LS,LF = CPM(Vt,E,TO)
    cp = findCPM(ES,EF,LS,LF)
    t = cp[-1][-1]
    sig = np.sqrt(np.sum([Vsig[i[0] - 1] for i in cp]))
    return t,sig

def runCPMfor(V,E,show_output = False):
    
    TO = topologicalSortKahn(V,E)
    ES,EF,LS,LF = CPM(V,E,TO)

    #wyświetlanie wyniku
    if(show_output):
        print("process time:")
        print(max(ES[-1],EF[-1],LS[-1],LF[-1]))
        print("earlyStart earlyFinish lateStart lateFinish:")
        for i in range (1, len(ES)-1):
            print(str(ES[i]) + " " + str(EF[i]) + " " + str(LS[i]) + " " + str(LF[i]))

    cpm = findCPM(ES,EF,LS,LF)
    if(show_output):
        print("critical path:")
        for i in range (0, len(cpm)):
            print(cpm[i][0],cpm[i][1],cpm[i][2]) 

    checkIfCorrectAnswer(filename,max(ES[-1],EF[-1],LS[-1],LF[-1]),ES[1:len(ES)-1],EF[1:len(ES)-1],LS[1:len(ES)-1],LF[1:len(ES)-1],cpm)



def checkIfCorrectAnswer(filename,pt,ES,EF,LS,LF,cpm):
    
    my_file = Path("./"+filename+".txt")
    
    if not my_file.is_file():
        my_file = Path("./CPM/"+filename+".txt")

    f = open(my_file, "r")
    
    line = f.readline()
    while(line[0] != "p"):
        line = f.readline()
    c_pt = f.readline()
    if(int(c_pt)!= pt):
        print("wrongPT")
        print("our:" + str(pt))
        print("should be: " + c_pt)
        return
    line = f.readline()
    for i in range(0,len(ES)):
        times = np.fromstring(f.readline(),sep=" ").astype(np.int16)
        if(ES[i] - times[0] != 0):
            print("Wrong ES in Job_" + str(i))
        if(EF[i] - times[1] != 0):
            print("Wrong EF in Job_" + str(i))
        if(LS[i] - times[2] != 0):
            print("Wrong LS in Job_" + str(i))
        if(LF[i] - times[3] != 0):
            print("Wrong LF in Job_" + str(i))

    f.readline()

    for i in range (0, len(cpm)):
        times = np.fromstring(f.readline(),sep=" ").astype(np.int16)
        if(cpm[i][1] - times[1] != 0 or cpm[i][0] - times[0] or cpm[i][2] - times[2]):
            print("Wrong CPM for " + filename) 
            return

    print("correct answer for " + filename)

    

def appendStartEnd(V,E):
    E_append = []
    for vind in range(1,len(V)+1):
        is_start = True
        is_end = True 
        for e in E: 
            if(is_end):
                if(e[0] == vind):
                    is_end = False
            if(is_start):
                if(e[1] == vind):
                    is_start = False
            if(not is_start and not is_end):
                break
        if(is_start):
            E_append = E_append + [[0,vind]]
        if(is_end):
            E_append = E_append + [[vind,len(V) + 1]]
    V = np.concatenate(([0], V))
    V = np.concatenate((V,[0]))
    return [0] + V + [0] , np.concatenate((E, E_append))


def CPM(V,E,TO):
    max_value = -1
    V,E = appendStartEnd(V,E)
    ES = [0] * len(V) #Early Start
    EF = [0] * len(V) #Early Finish
    for v_i in TO:#range(0,len(V)): # v_i - V index 
        for e in E:
            if e[1] == v_i:
                max_value = max(ES[v_i],EF[e[0]])
                ES[v_i] = max(ES[v_i],EF[e[0]])
        EF[v_i] = ES[v_i] + V[v_i]
    LS = [max_value] * len(V) #Late Start
    LF = [max_value] * len(V) #LateFinish
    for v_i in reversed(TO):#reversed(range(0,len(V))): # v_i - V index 
        for e in E:
            if e[0] == v_i:
                LF[v_i] = min(LF[v_i],LS[e[1]])
        LS[v_i] = LF[v_i] - V[v_i] 
    return ES,EF,LS,LF



def findCPM(ES,EF,LS,LF):
    cpm = []
    for i in range (1, len(ES)-1):
        if ES[i] == LS[i]:
            cpm.append([i,ES[i],EF[i]])
    cpm = sorted(cpm, key=lambda x: x[1])
    return cpm



t,sig = runPERTfor("pert_wzor")

print(dystrybuanta(17,t,sig))

print(dystrybuantaODWR(99,t,sig))

















