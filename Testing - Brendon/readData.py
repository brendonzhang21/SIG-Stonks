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

tradingDays = len(prcAll[0])
instruments = len(prcAll)
correlationCoef = [[] for _ in range(instruments)]
totalMarketCap = []
runningAverageArray = [[] for _ in range(instruments)]
runningAverage = [[] for _ in range(instruments)]
marketRunningAverageArray = []
marketRunningAverage = []
dayChangeInstRunAvg = [[] for _ in range(instruments)]
dayChangeMktRunAvg = []
runningAverageLength = 5

# Calculate the Daily Market Cap
for day in range(tradingDays):
    mcp = 0
    for inst in range(len(prcAll)):
        mcp += prcAll[inst][day]
        #print(mcp)
    totalMarketCap.append(mcp)

# Calculate the Correlation Coefficient between stocks
for i in range(instruments):
    if i > 0:
        for indexPos in range(i):
            correlationCoef[i].append(correlationCoef[indexPos][i])
            
    for j in range(i, instruments):
        if j == i:
            currentCorrelation = 0
        else:
            currentCorrelation = np.corrcoef(prcAll[i],prcAll[j])[0][1]
            
        if currentCorrelation > 0.4 or currentCorrelation < -0.4:
            correlationCoef[i].append(currentCorrelation)
        else:
            correlationCoef[i].append(0)

# Calculate the running average of each trading instrument and the market
for day in range(tradingDays):

    marketRunningAverageArray.append(totalMarketCap[day])

    if day < runningAverageLength - 1:
        marketRunningAverage.append(0)
    else:
        marketRunningAverage.append(np.mean(marketRunningAverageArray))
        marketRunningAverageArray.pop(0)

    for instrument in range(instruments):
        runningAverageArray[instrument].append(prcAll[instrument][day])
        if day < runningAverageLength - 1:
            runningAverage[instrument].append(0)
        else:
            runningAverage[instrument].append(np.mean(runningAverageArray[instrument]))
            runningAverageArray[instrument].pop(0)

# Calculate the change in running average of market and stocks

for i in range(len(marketRunningAverage)):
    if i < runningAverageLength:
        dayChangeMktRunAvg.append(0)
    else:
        dayChangeMktRunAvg.append(marketRunningAverage[i] / marketRunningAverage[i-1] - 1)

    for instrument in range(instruments):
        if i < runningAverageLength:
            dayChangeInstRunAvg[instrument].append(0)
        else:
            dayChangeInstRunAvg[instrument].append(runningAverage[instrument][i] / runningAverage[instrument][i - 1] - 1)
 
# print(runningAverage[0])
# for day in range(tradingDays):
#     if day >= runningAverageLength - 1:
#         # start trading
#         #compare instrument to the market
#         for instrument in range(instruments):

# print(dayChangeInstRunAvg[0])
    # for inst in range(len(prcAll)):
    #     inst_mcp = prcAll[inst][day] / mcp
    #     if day == 0:
    #         print(inst_mcp)
    #find market cap for each instrument
    # determine position based on current share price vs mean