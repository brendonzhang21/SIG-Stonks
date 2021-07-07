import numpy as np
from numpy.lib.function_base import corrcoef
import pandas as pd

# Obtaining data from .txt file and converting to float
def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

pricesFile="./prices250.txt"
prcAll = loadPrices(pricesFile)
print ("Loaded %d instruments for %d days" % (nInst, nt))

correlationCoef = [[] for _ in range(len(prcAll))]
# print(len(correlationCoef))

for i in range(len(prcAll)):
    if i > 0:
        for indexPos in range(i):
            correlationCoef[i].append(correlationCoef[indexPos][i])
            
    for j in range(i, len(prcAll)):
        if j == i:
            currentCorrelation = 0
        else:
            currentCorrelation = np.corrcoef(prcAll[i],prcAll[j])[0][1]
            
        if currentCorrelation > 0.4 or currentCorrelation < -0.4:
            correlationCoef[i].append(currentCorrelation)
        else:
            correlationCoef[i].append(0)

print(prcAll)

# print(correlationCoef[-2])
# print(len(correlationCoef[0]))
# print(max(correlationCoef[0]), min(correlationCoef[0]))
# highCorr = correlationCoef[0].index(min(correlationCoef[0]))
# print(highCorr + 1)