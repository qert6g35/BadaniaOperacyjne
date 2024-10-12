from cpmLab import loadData

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
    return [0] + V + [0] , E + E_append


def CPM(V,E):
    max_value = -1
    V,E = appendStartEnd(V,E)
    finish = False
    ES = [0] * len(V) #Early Start
    EF = [0] * len(V) #Early Finish
    detected_change = True
    while(detected_change):
        detected_change = False
        for v_i in range(0,len(V)): # v_i - V index 
            for e in E:
                if e[1] == v_i:
                    max_value = max(ES[v_i],EF[e[0]])
                    temp = max(ES[v_i],EF[e[0]])
                    if temp != ES[v_i]:
                        ES[v_i] = temp
                        detected_change = True
            temp = ES[v_i] + V[v_i]
            if temp != EF[v_i]:
                EF[v_i] = temp
                detected_change = True
    LS = [max_value] * len(V) #Late Start
    LF = [max_value] * len(V) #LateFinish
    detected_change = True
    while(detected_change):
        detected_change = False
        for v_i in reversed(range(0,len(V))): # v_i - V index 
            for e in E:
                if e[0] == v_i:
                    temp = min(LF[v_i],LS[e[1]])
                    if temp != LF[v_i]:
                        LF[v_i] = temp
                        detected_change = True
            temp = LF[v_i] - V[v_i] 
            if temp != LS[v_i]:
                LS[v_i] = temp
                detected_change = True

    return ES,EF,LS,LF

#pobieranie danych

V,E = loadData("data10")

#rozwiązywanie problemu

ES,EF,LS,LF = CPM(V,E)


#wyświetlanie wyniku

print("process time:")
print(max(ES[-1],EF[-1],LS[-1],LF[-1]))
print("earlyStart earlyFinish lateStart lateFinish:")
for i in range (1, len(ES)-1):
    print(str(ES[i]) + " " + str(EF[i]) + " " + str(LS[i]) + " " + str(LF[i]))
