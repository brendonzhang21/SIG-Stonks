# Trading based on RSI and divergence?

import numpy as np
from numpy.core.arrayprint import printoptions

nInst=100
currentPos = np.zeros(nInst)
rsiPeriod = 14
rsiUpperBound = 70
rsiLowerBound = 30
instLimit = 10000

def getMyPosition(prcSoFar):
    global currentPos
    
    numDays = len(prcSoFar[0])
    instRSIarray = []

    if numDays >= rsiPeriod:
        currentPos = np.ones(nInst)
        
        for inst in range(nInst):

            instGain = 0
            instLoss = 0

            for day in range(numDays - rsiPeriod + 1, numDays):
                dayChange = prcSoFar[inst][day] - prcSoFar[inst][day - 1]

                if dayChange > 0:
                    instGain += dayChange
                else:
                    instLoss += abs(dayChange)

            avgGain = instGain / rsiPeriod
            avgLoss = instLoss / rsiPeriod
            if avgLoss == 0:
                instRSI = 100
            else:
                instRelStrength = avgGain/avgLoss
                instRSI = 100 - 100/(1 + instRelStrength)

            instRSIarray.append(instRSI)

            if instRSI > rsiUpperBound:
                currentPos[inst] = 0
            elif instRSI < rsiLowerBound:
                currentPos[inst] = instLimit / prcSoFar[inst][-1]
            else:
                scaled = (instRSI - rsiLowerBound) / (rsiUpperBound - rsiLowerBound)
                currentPos[inst] = (instLimit * (1-scaled)) / prcSoFar[inst][-1]
    else:
        print("Day " + str(numDays))
        currentPos = np.zeros(nInst)

    return currentPos