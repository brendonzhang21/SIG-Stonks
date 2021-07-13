import numpy as np
instLimit = 10000

def getMyPosition (prcSoFar):

    (nins,nt) = prcSoFar.shape
    rpos = np.array([0 for i in range(100)])
    runningAverageTime = 8
    for instrument in range(nins):
        if nt > 1:
            stdev = np.std(prcSoFar[instrument][nt - runningAverageTime:nt])
            if stdev == 0:
                z = 0
            else:
                z = (prcSoFar[instrument][nt-1] - np.mean(prcSoFar[instrument][nt - runningAverageTime:nt]))/stdev

            if z > 1:
                rpos[instrument] = -instLimit/prcSoFar[instrument][nt-1]
            elif z < -1:
                rpos[instrument] = instLimit/prcSoFar[instrument][nt-1]
            elif z < 0 or z > 0:
                rpos[instrument] = -instLimit * z / prcSoFar[instrument][nt-1]
            else: 
                rpos[instrument] = 0
    return rpos