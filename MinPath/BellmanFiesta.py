import numpy as np
import math
import random as rnd
from pathlib import Path
import scipy.stats as st
from DataManagment import loadData

def BellMyFord(DistMat):
    problemSize = len(DistMat)
    ans = np.zeros(problemSize).astype(int)
    ansTable = [[0]]
    for _ in range(1,problemSize):
        ansTable += [[]]
    #print(ansTable)
    ans += 999999999
    ans[0] = 0
    changed = True
    #print(ans)
    while(changed):
        changed = False
        for mainID in range(0,problemSize):
            for checkedID in range(0,problemSize):
                if(mainID == checkedID or DistMat[checkedID][mainID] == 0):
                    continue
                # print("checking point",mainID," for shortest distance to",checkedID)
                # print("ans to:",mainID," PRE swap is:",ans[mainID])
                # print("we checking ")
                new_ans = min(DistMat[checkedID][mainID] + ans[checkedID],ans[mainID])
                if(new_ans != ans[mainID]):
                    ansTable[mainID] = ansTable[checkedID] + [mainID]
                    ans[mainID] = new_ans
                    changed = True
                # print("ans to:",mainID," POST swap is:",ans[mainID])
    return ans,ansTable

# print(BellMyFord(loadData("MData5")))