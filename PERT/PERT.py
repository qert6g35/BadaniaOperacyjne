import numpy as np
import math
import random as rnd
from pathlib import Path
from pertTools import loadData, topologicalSortKahn
import scipy.stats as st

def GenerateData(n,n_instance,use_m_data = False,prep_data_type = 0,Vt_sent = None,Vsig_sent = None): 
    #
    # args:
    # n - ile danych chcemy wygenerować
    # n_instance - jak dużą instancję chcemy wygenerować
    # prep_data_type [int] in (0,1,2):
    #   0 - generujemy 3 losowe dane i je wysw
    #   1 - generujemy średni czas i odchylenie od niego które jest identyczne dla opuźnienia i przyśpieszenia wykonania zadania
    #   2 - generujemy średni czas i dwa odchylenia które osobno są średni czas + odchylenie1 jako najpuźniejszy czas wykonania, oraz średni czas - odchylenie2 jako njwcześniejszy czas wykonania,
    #
    # return:
    # T,SIG - wiadomo theta i sigma wygenerowanej instancji
    #  Data - wygenerowane czasy zakończeń
    Data = np.array([])
    if(use_m_data):
        V_data,E = loadData("pert_wzor")
    else:
        if(prep_data_type == 0):
            V_data,E = prepData(n_instance)
        elif(prep_data_type == 1):
            V_data,E = prepDataOnDisturbtion(n_instance,False)
        else:
            V_data,E = prepDataOnDisturbtion(n_instance,True)
    if(Vt_sent == None):
        Vt = [ (v[0] + v[1]*4 + v[2])/6 for v in V_data]
    else:
        Vt = Vt_sent
    if(Vsig_sent == None):
        Vsig = [ np.power((-v[0] + v[2])/6,2) for v in V_data]
    else:
        Vsig = Vsig_sent

    t, sig = runPERTfor(Vt,Vsig,E)
    # print("t,sig:")
    # print(t,",",sig)
    for _ in range(0,n):
        V_instance = getInstance(V_data)
        # V_instance = getInstance(Vt,Vsig)
        Data = np.append(Data,runCPMfor(V_instance,E))
    
    # print(dystrybuanta(17,t,sig))
    # print(dystrybuantaODWR(99,t,sig))

    return t,sig,Data
    
    

def prepData(number_of_V):
    V = []
    E = []
    for v_count in range(0, number_of_V):
        # help = [rnd.randrange(10,50),rnd.randrange(10,50),rnd.randrange(10,50)]
        help = []
        while len(help) < 3:
            val = rnd.randrange(10,50)
            if val not in help:
                help.append(val)
        help.sort()
        V = V + [help]
        #print(V)
        if(v_count > 0):
            for _ in range(0,math.floor(math.sqrt(v_count + 1))):
                #print(E)
                connection = [rnd.randrange(0,v_count) + 1,v_count + 1]
                E = E + [connection]
                #print(E)
    return V,E

def prepDataOnDisturbtion(number_of_V,use_diffrent_disturption = False):
    #
    # generujemy dane jako
    # 1. określamy średnie wykonanie 
    # 2. losujemy o ile projekt może być przyśpieszony jako procent czasu trwania + 1
    # 3. jeżeli use_diffrent_disturption == true to czas opużnienia generujey osobno jak nie to bierzy tą samą co do przyśpieszenia
    # 
    # 
    #
    V = []
    E = []
    for v_count in range(0, number_of_V):
        v_mean = rnd.randrange(10,50)
        v_distubtion_p = rnd.randrange(1,math.ceil(v_mean * 0.2) + 1)
        v_distubtion_m = v_distubtion_p
        if(use_diffrent_disturption):
            v_distubtion_m = rnd.randrange(1,math.ceil(v_mean * 0.2) + 1)
        V = V + [[v_mean - v_distubtion_m ,v_mean,v_mean + v_distubtion_p]]
        #print(V)
        if(v_count > 0):
            for _ in range(0,math.floor(math.sqrt(v_count + 1))):
                #print(E)
                connection = [rnd.randrange(0,v_count) + 1,v_count + 1]
                E = E + [connection]
                #print(E)
    return V,E

def getInstanceNorm(Vt,Vsig):
    newV = np.array([])
    for id in range(0,len(Vt)):
        newV = np.append(newV, rnd.normalvariate(Vt[id],math.sqrt(Vsig[id])))
    return newV

def getInstance(V):
    newV = np.array([])
    for id in range(0,len(V)):
        # print("V:" + str(V[id]))
        # print("0:" + str(V[id][0]))
        # print("1:" + str(V[id][1]))
        # print("2:" + str(V[id][2]))
        newV = np.append(newV, np.random.triangular(V[id][0],V[id][1],V[id][2]))
    return newV

def dystrybuantaODWR(X,t,sig):# UWAGA X PODAJESZ JAKO NUMBER in (0-100)
    return st.norm.ppf(q=X/100,loc=t,scale=sig)

def dystrybuanta(X,t,sig):# UWAGA X PODAJESZ JAKO NUMBER in (0-100)
    return st.norm.cdf((X - t)/sig)*100

def runPERTfor(Vt,Vsig,E): # zwraca theta i sig dla podanych danych
    # print(Vt)
    # print(Vsig)
    #TO = topologicalSortKahn(Vt,E)
    ES,EF,LS,LF = CPM(Vt,E)
    cp = findCPM(ES,EF,LS,LF)
    t = cp[-1][-1]
    sig = np.sqrt(np.sum([Vsig[i[0] - 1] for i in cp]))
    return t,sig

def runCPMfor(V,E): # zwraca czas wykonania dla podanego przykładu
    ES,EF,LS,LF = CPM(V,E)
    return max(ES[-1],EF[-1],LS[-1],LF[-1])

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


def CPM(V,E):
    max_value = -1
    V,E = appendStartEnd(V,E)
    ES = [0] * len(V) #Early Start
    EF = [0] * len(V) #Early Finish
    for v_i in range(0,len(V)): # v_i - V index 
        for e in E:
            if e[1] == v_i:
                max_value = max(ES[v_i],EF[e[0]])
                ES[v_i] = max(ES[v_i],EF[e[0]])
        EF[v_i] = ES[v_i] + V[v_i]
    LS = [max_value] * len(V) #Late Start
    LF = [max_value] * len(V) #LateFinish
    for v_i in reversed(range(0,len(V))): # v_i - V index 
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
    # print(cpm)
    return cpm
