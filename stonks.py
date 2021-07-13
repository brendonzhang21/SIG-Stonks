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

def getMyPosition (prcSoFar):

    (nins,nt) = prcSoFar.shape
    rpos = np.array([0 for i in range(100)])

    zscores = []
    x = 8
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
            else: 
                rpos[instrument] = 0
    return rpos
