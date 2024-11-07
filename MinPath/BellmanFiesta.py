import numpy as np
import math
import random as rnd
from pathlib import Path
import scipy.stats as st
from DataManagment import loadData

def BellMyFord(DistMat):
    problemSize = len(DistMat)
    ans = np.zeros(problemSize).astype(int)
    changed = True
    while(changed):
        changed = False
        for mainID in range(0,problemSize):
            for checkedID in range(0,problemSize):
                ans += 1
                if(mainID == checkedID):
                    continue


    return ans

print(BellMyFord(loadData("MData5")))