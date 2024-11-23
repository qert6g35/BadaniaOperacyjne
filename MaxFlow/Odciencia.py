import numpy as np
import math
import random as rnd
from pathlib import Path
import scipy.stats as st
from DataManagment import loadData

from collections import defaultdict

def Greed1MinCut(MaxFlows,source,sink,show_prompts):
    minCut = 99999999
    nodes_to_cut = [ i for i in range(0, len(MaxFlows)) if i != source and i != sink]
    nodes_cuted = [sink]
    minCut = CalcCutValue(MaxFlows,nodes_cuted,nodes_to_cut + [source])
    if minCut == None:
        if show_prompts:
            print("Failed sink not connected to rest of graph")
        return 0
    while len(nodes_to_cut)> 0:
        # define witch point to cut
        currentMin = 999999999
        currentPointToCut = -1
        for i in nodes_to_cut: #            z pośród punkótw do wyciecia
            if len([j for j in nodes_cuted if MaxFlows[i][j] != 0 ]) > 0: #które mają trasę do jakiegokolwiek uciętego pkt
                # if i == 2:
                #     print([j for j in nodes_cuted if MaxFlows[i,j] != 0 ])
                cut = CalcCutValue(MaxFlows,nodes_cuted + [i],[a for a in nodes_to_cut + [source] if a != i])
                if cut != None:
                    new_min = min(currentMin,cut)
                    # if i == 2:
                    #     print("new_min",new_min)
                    #     print(CalcCutValue(MaxFlows,nodes_cuted + [i],[a for a in nodes_to_cut + [source] if a != i]))
                    if(new_min < currentMin):
                        currentMin = new_min
                        currentPointToCut = i
                #print("we can cut:",i)
        if currentPointToCut == -1:
            if show_prompts:
                print("Failed to pick next point to cut")
                print("nodes_to_cut:",nodes_to_cut)
                print("nodes_cuted:",nodes_cuted)
            if CalcCutValue(MaxFlows,nodes_cuted + [i],[a for a in nodes_to_cut + [source] if a != i]) == None:
                return 0
            return minCut
        # print("nodes_to_cut:",nodes_to_cut)
        # print("nodes_cuted:",nodes_cuted)
        nodes_to_cut += [currentPointToCut]
        nodes_to_cut.remove(currentPointToCut)
        minCut = min(minCut,currentMin)
      
    return minCut

def Greed2MinCut(MaxFlows,source,sink,show_prompts):
    nodes_to_cut = [ i for i in range(0, len(MaxFlows)) if i != source and i != sink]
    nodes_cuted = [sink]
    minCut = CalcCutValue(MaxFlows,nodes_cuted,nodes_to_cut + [source])
    if minCut == None:
        if show_prompts:
            print("Failed sink not connected to rest of graph")
        return 0
    while len(nodes_to_cut)> 0:
        # define witch point to cut
        currentMax = -999999999
        currentPointToCut = -1
        for i in nodes_to_cut: #            z pośród punkótw do wyciecia
            paths_to_i = [MaxFlows[i][j] for j in nodes_cuted if MaxFlows[i][j] != 0 ]
            if nodes_cuted == [24, 22, 19, 20, 18, 23, 17, 15, 16, 21, 14, 10, 12, 13, 11, 8, 5, 9, 6, 1, 7, 3, 4] and nodes_to_cut == [2]:
                print(paths_to_i)
            if len(paths_to_i) > 0: #które mają trasę do jakiegokolwiek uciętego pkt
                new_max = max(currentMax,sum(paths_to_i))
                if(new_max > currentMax):
                    # print("new_max",new_max)
                    # print("currentMax",currentMax)
                    currentMax = new_max
                    currentPointToCut = i
                #print("we can cut:",i)
        if (currentPointToCut == -1 or currentMax <= 0): 
            if show_prompts:
                print("Failed to pick next point to cut")
                print("nodes_to_cut:",nodes_to_cut)
                print("nodes_cuted:",nodes_cuted)
            return minCut 
        # print("we cutting:"+str(currentPointToCut))
        # print("nodes_to_cut:",nodes_to_cut)
        # print("nodes_cuted:",nodes_cuted)
        nodes_cuted += [currentPointToCut]
        nodes_to_cut.remove(currentPointToCut)
        new_cut_value = CalcCutValue(MaxFlows,nodes_cuted,nodes_to_cut + [source])
        if new_cut_value == None:
            if show_prompts:
                print("nodes_cuted NOT CONNECTED TO nodes_to_cut")
                print("nodes_to_cut:",nodes_to_cut)
                print("nodes_cuted:",nodes_cuted)
            return 0 
        minCut = min(minCut,new_cut_value)
      
    return minCut

def CalcCutValue(MaxFlows,cuted,not_cuted):
    sum = 0
    for i in cuted:
        for j in not_cuted:
            sum += MaxFlows[j][i]
    if sum == 0:
        return None
    return sum

# graph = loadData("/Examples/5")
# print(Greed1MinCut(graph,0,len(graph)-1,True))
# print(Greed2MinCut(graph,0,len(graph)-1,True))