from cpmLab import loadData

V = [5,5,5]
E = [[0,1],[1,2]]


def CPM(V,E):
    finish = False
    ES = [0] * len(V) #Early Start
    EF = [0] * len(V) #Early Finish
    LS = [0] * len(V) #Late Start
    LF = [0] * len(V) #LateFinish

    print("ES")
    print(ES)
    print("EF")
    print(EF)

    while(finish == False):
        finish = True
        for v_i in range(0,len(V)): # v_i - V index 
            for e in E:
                if e[1] == v_i:
                    ES[v_i] = max(ES[v_i],EF[e[0]])
            EF[v_i] = ES[v_i] + V[v_i]

    return ES,EF,LS,LF
        
V,E = loadData("dataSort10")
for e in E:
    e[0] -= 1
    e[1] -= 1
CPM(V,E)