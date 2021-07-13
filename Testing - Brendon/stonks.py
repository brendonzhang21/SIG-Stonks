#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np
from numpy.core.arrayprint import printoptions

nInst=100
currentPos = np.zeros(nInst)
runningAverageLength = 8
maxPosition = 10000
maxMktChange = 0.0268
minMktChange = -0.0305

# Dummy algorithm to demonstrate function format.
def getMyPosition (prcSoFar):
    global currentPos
    # (nins,nt) = prcSoFar.shape
    # rpos = np.array([int(x) for x in 1000 * np.random.randn(nins)])
    # currentPos += rpos

    numDays = len(prcSoFar[0])
    marketCap = []
    instMovAvgChange = []
    mktMovAvgChange = 0
    currentMktMovAvg = 0
    prevMktMovAvg = 0

    # Start Trading on Day (RunningAverageLength + 1) as we now have sufficient data
    if numDays > runningAverageLength:
        print("---- Day " + str(numDays) + " ----")
        for day in range(numDays - runningAverageLength - 1, numDays):
            mcp = 0
            for inst in range(nInst):
                mcp += prcSoFar[inst][day]
            marketCap.append(mcp)
        
        currentMktMovAvg = np.mean(marketCap[1:])
        prevMktMovAvg = np.mean(marketCap[0:-1])
        mktMovAvgChange = currentMktMovAvg / prevMktMovAvg - 1

        for inst in range(nInst):
            instCurrentAvg = np.mean(prcSoFar[inst][numDays - runningAverageLength:])
            instPrevAvg = np.mean(prcSoFar[inst][numDays - runningAverageLength - 1:-1])
            instMovAvgChange.append(instCurrentAvg / instPrevAvg - 1)

        
        # Compare the moving average of instrument vs market
        if mktMovAvgChange > 0:
            currentPos = np.zeros(nInst)
        else:
            if mktMovAvgChange > minMktChange / 2:
                position = maxPosition / 2
            else:
                position = maxPosition

            for inst in range(nInst):
                instPost = position / prcSoFar[inst][-1]
                currentPos[inst] = int(instPost)

        # print(currentPos)
    else:
        print("Day " + str(numDays) + " = 0")

    # print(mktMovAvgChange)
    
    return currentPos

    
