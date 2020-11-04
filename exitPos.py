#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      George
#
# Created:     14/10/2020
# Copyright:   (c) George 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from config import tradeName,entryPrice,entryQuant,myBPV,cumuProfit,mp,profit
from tradeClass import tradeInfo

def exitPos(myExitPrice,myExitDate,tempName,myCurShares):
    profit = 0
    if mp < 0:
        trades = tradeInfo('liqShort',myExitDate,tempName,myExitPrice,myCurShares,0)
        profit = trades.calcTradeProfit('liqShort',mp,entryPrice,myExitPrice,entryQuant,myCurShares) * myBPV
        profit = profit - myCurShares *commission;trades.tradeProfit = profit;cumuProfit += profit
        trades.cumuProfit = cumuProfit
    else:
        trades = tradeInfo('liqLong',myExitDate,tempName,myExitPrice,myCurShares,0)
        profit = trades.calcTradeProfit('liqLong',mp,entryPrice,myExitPrice,entryQuant,myCurShares) * myBPV
        profit = profit - myCurShares * commission;trades.tradeProfit = profit;cumuProfit += profit
        trades.cumuProfit = cumuProfit
    curShares = 0
    for remShares in range(0,len(entryQuant)):curShares += entryQuant[remShares]
    return (profit,trades,curShares)
