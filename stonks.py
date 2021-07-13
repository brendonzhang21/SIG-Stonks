#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.
import numpy as np
from numpy.lib.function_base import average
from numpy.ma.core import MaskedIterator
import pandas as pd
import math
nInst = 100
instLimit = 10000

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
    # diff = []
    # positions = [0]
    # totalprofit = 0
    
    # for day in range(len(prcSoFar[0])):
    #     for inst in range(len(prcSoFar)):
    #         prevAvg = np.mean(prcSoFar[inst][0:day])
    #         diff.append(prcSoFar[inst][day] - prevAvg)

    #         if  prcSoFar[inst][day] > prevAvg and day != 0:
    #             #fix this - can only sell max what we hold 
    #             sellamount = positions[day-1]
    #             profit = sellamount * prcSoFar[inst][day]
    #             totalprofit += profit 
    #             positions.append(0)
    #             #print("selling")

    #         elif  prcSoFar[inst][day] < prevAvg and day != 0:
    #             buyamount = 10000 / prcSoFar[inst][day]
    #             cost = buyamount * prcSoFar[inst][day]
    #             totalprofit -= cost
    #             positions.append(buyamount)
    #             #print("buying")


    # print(totalprofit)   

    (nins,nt) = prcSoFar.shape


    #METHOD 1: mean reversion 
    individualReturns = []
    #rpos is a 100 element array for daily positions of all instruments - tb returend 
    rpos = np.array([0 for i in range(100)])
    # for instrument in range(nins):
    #     individualReturns.append((prcSoFar[instrument][nt-1] - prcSoFar[instrument][nt-2]) / prcSoFar[instrument][nt-1])  
    # marketReturn = sum(individualReturns)/nInst 
    # print(individualReturns)
    #print(marketReturn)


    #METHOD 2: calculate z score for each instrument and use it to determine positiion
    zscores = []
    x = nt
    for instrument in range(nins):
        if nt > 1:
            stdev = np.std(prcSoFar[instrument][nt - x:nt])
            if stdev == 0:
                z = 0
            else:
                z = (prcSoFar[instrument][nt-1] - np.mean(prcSoFar[instrument][nt - x:nt]))/np.std(prcSoFar[instrument][nt - x:nt])
            zscores.append(z)

            if z > 1:
                rpos[instrument] = -10000/prcSoFar[instrument][nt-1]
            elif z < -1:
                rpos[instrument] = 10000/prcSoFar[instrument][nt-1]
            elif z < 0 or z > 0:
                rpos[instrument] = -10000 * z / prcSoFar[instrument][nt-1]
            elif z > 0:
                rpos[instrument] = -(10000 * abs(z)) / prcSoFar[instrument][nt-1]
            else: 
                rpos[instrument] = 0
                print("Hello")
                print('Day ' + str(nt) + ' z ' + str(z))
            # if pd.isna(z):
            # print(max(zscores))
            #     print(np.mean(prcSoFar[instrument][:nt]), np.std(prcSoFar[instrument][:nt]))
  # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    # print("z scores:", zscores)
    # print("position",rpos)

    return rpos

    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.