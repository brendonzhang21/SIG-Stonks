#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np
import pandas as pd
import math

nInst=100
currentPos = np.zeros(nInst)

def loadPrices(fn):
    global nt, nInst
    df= pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

pricesFile="./prices250.txt"

#prcSoFar [Instrument][Day]
#prcAll = loadPrices(pricesFile)
#print ("Loaded %d instruments for %d days" % (nInst, nt))

#print(prcAll)
# Dummy algorithm to demonstrate function format.
def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    rpos = np.array([int(x) for x in 1000 * np.random.randn(nins)])
    currentPos += rpos
    

    #find market cap for everyday
    #totalmarketCap = []
    #for day in range(len(prcAll[0])):
    #    mcp = 0
    #    for inst in range(len(prcAll)):
    #        mcp += prcAll[inst][day]
    #        #print(mcp)
    #    totalmarketCap.append(mcp)

    #    for inst in range(len(prcAll)):
    #        inst_mcp = prcAll[inst][day] / mcp
    #        if day == 0:
    #            print(inst_mcp)

    #print(totalmarketCap)
    diff = []
    positions = [0]
    totalprofit = 0
    
    for day in range(len(prcSoFar[0])):
        for inst in range(len(prcSoFar)):
            prevAvg = np.mean(prcSoFar[inst][0:day])
            diff.append(prcSoFar[inst][day] - prevAvg)

            if  prcSoFar[inst][day] > prevAvg and day != 0:
                #fix this - can only sell max what we hold 
                sellamount = positions[day-1]
                profit = sellamount * prcSoFar[inst][day]
                totalprofit += profit 
                positions.append(0)
                #print("selling")

            elif  prcSoFar[inst][day] < prevAvg and day != 0:
                buyamount = 10000 / prcSoFar[inst][day]
                cost = buyamount * prcSoFar[inst][day]
                totalprofit -= cost
                positions.append(buyamount)
                #print("buying")


    print(totalprofit)   

    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    return currentPos