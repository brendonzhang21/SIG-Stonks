# Same as eval but creates an output.txt file to help visualise results
# Also I changed line 44 and 45 + commented out some other things
# Original is the commented out line, new for loop i wrote so we can use out own data


import numpy as np
import pandas as pd
from stonks2 import getMyPosition as getPosition
import os

# Algorithm testing file. 
# Quantitative judging will be determined from output of this program.
# Judging will use unseeen, future price data from the same universe.

nInst = 0
nt = 0

# Commission rate.
commRate = 0.0050

# Dollar position limit (maximum absolute dollar value of any individual stock position).
dlrPosLimit = 10000

def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

pricesFile="./prices250.txt"
prcAll = loadPrices(pricesFile)
print ("Loaded %d instruments for %d days" % (nInst, nt))

def calcPL(prcHist):
    cash = 0
    curPos = np.zeros(nInst)
    totDVolume = 0
    totDVolume0 = 0
    totDVolume1 = 0
    frac0 = 0.
    frac1 = 0.
    value = 0
    todayPLL = []
    (_,nt) = prcHist.shape
    f = open("output.txt", 'a')
    # for t in range(201,251):
    for t in range(1,251):
        prcHistSoFar = prcHist[:,:t]
        newPosOrig = getPosition(prcHistSoFar)
        curPrices = prcHistSoFar[:,-1] 
        posLimits = np.array([int(x) for x in dlrPosLimit / curPrices])
        newPos = np.array([int(p) for p in np.clip(newPosOrig, -posLimits, posLimits)])
        deltaPos = newPos - curPos
        dvolumes = curPrices * np.abs(deltaPos)
        dvolume0 = np.sum(dvolumes[:50])
        dvolume1 = np.sum(dvolumes[50:])
        dvolume = np.sum(dvolumes)
        totDVolume += dvolume
        totDVolume0 += dvolume0
        totDVolume1 += dvolume1
        comm = dvolume * commRate
        cash -= curPrices.dot(deltaPos) + comm
        curPos = np.array(newPos)
        posValue = curPos.dot(curPrices)
        todayPL = cash + posValue - value
        todayPLL.append(todayPL)
        value = cash + posValue
        ret = 0.0
        if (totDVolume > 0):
            ret = value / totDVolume
            frac0 = totDVolume0 / totDVolume
            frac1 = totDVolume1 / totDVolume
        f.write("Day %d value: %.2lf todayPL: $%.2lf $-traded: %.0lf return: %.5lf frac0: %.4lf frac1: %.4lf\n" % (t,value, todayPL, totDVolume, ret, frac0, frac1))
        #print ("Day %d value: %.2lf todayPL: $%.2lf $-traded: %.0lf return: %.5lf frac0: %.4lf frac1: %.4lf" % (t,value, todayPL, totDVolume, ret, frac0, frac1))
    pll = np.array(todayPLL)
    (plmu,plstd) = (np.mean(pll), np.std(pll))
    annSharpe = 0.0
    if (plstd > 0):
        annSharpe = 16 * plmu / plstd
    f.close()
    return (plmu, ret, annSharpe, totDVolume)

# Output.
if os.path.exists("output.txt"):
    os.remove("output.txt")
else:
    print("No File to Remove")
(meanpl, ret, sharpe, dvol) = calcPL(prcAll)
f = open("output.txt", 'a')
f.write("=====\n")
f.write("mean(PL): %.0lf\n" % meanpl)
f.write("return: %.5lf\n" % ret)
f.write("annSharpe(PL): %.2lf \n" % sharpe)
f.write("totDvolume: %.0lf \n" % dvol)
f.close()

# print ("=====")
# print ("mean(PL): %.0lf" % meanpl)
# print ("return: %.5lf" % ret)
# print ("annSharpe(PL): %.2lf " % sharpe)
# print ("totDvolume: %.0lf " % dvol)



