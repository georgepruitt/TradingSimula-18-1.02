#-------------------------------------------------------------------------------
# Name:        utilityFunctions
# Purpose:
#
# Author:      George Pruitt
#
# Created:     21/10/2016
# Copyright:   (c) George 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
from math import trunc,log10
from datetime import date

def getDataAtribs(dClass):
   return(dClass.bigPtVal,dClass.symbol,dClass.longName,dClass.minMove)
def getDataLists(dClass):
   return(dClass.date,dClass.open,dClass.high,dClass.low,dClass.close)
def roundToNearestTick(price,upOrDown,tickValue):
    temp1 = price - int(price)
    temp2 = int(temp1 / tickValue)
    temp3 = temp1 -(tickValue*temp2)
    if upOrDown == 1:
        temp4 = tickValue - temp3
        temp5 = temp1 + temp4
    if upOrDown == -1:
        temp4 = temp1 - temp3
        temp5 = temp4
    return(int(price) + temp5)

def crosses(price,level,overOrBelow,bar):
   result = 0
   if overOrBelow == 1:
      if price[bar-1] < level and price[bar] >= level:
         result = 1
   if overOrBelow == -1:
      if price[bar-1] > level and price[bar] <= level:
         result = 1
   return result

def calcAvgLongShort(listOfTrades,numOfLastTrades):
    avgBuy = 0;numBuys = 0
    avgSell = 0;numSells = 0
    numOfLastTrades *=2
    if len(listOfTrades) >= numOfLastTrades+1:
        for trds in range(len(listOfTrades)- (numOfLastTrades+1), len(listOfTrades)-1):
    #        print(tempTrdList[trds].tradeDate," ",tempTrdList[trds].tradeName," ",tempTrdList[trds].tradePrice," ",tempTrdList[trds].tradeOrder)
    #        print(listOfTrades[trds].tradeName)
            if listOfTrades[trds].entryOrExit == 0:
                if listOfTrades[trds].tradeOrder == 'liqLong' or listOfTrades[trds].tradeOrder == 'L-EOD':
                    avgBuy+=listOfTrades[trds].tradeProfit;numBuys+=1
                if listOfTrades[trds].tradeOrder == 'liqShort' or listOfTrades[trds].tradeOrder == 'S-EOD':
                    avgSell+=listOfTrades[trds].tradeProfit;numSells+=1
        if numBuys > 0: avgBuy /= numBuys
        if numSells > 0: avgSell/= numSells
    return(avgBuy,avgSell,numBuys,numSells)


def calcTodaysOTE(mp,myClose,entryPrice,entryQuant,myBPV):
    todaysOTE = 0
    for entries in range(0,len(entryPrice)):
        if mp >= 1: todaysOTE += (myClose - entryPrice[entries])*myBPV*entryQuant[entries]
        if mp <= -1: todaysOTE += (entryPrice[entries] - myClose)*myBPV*entryQuant[entries]
    return(todaysOTE)

def removeDuplicates(li):
    my_set = set()
    res = []
    for e in li:
        if e not in my_set:
            res.append(e)
            my_set.add(e)
    return res

def setDataLists(dClass):
    d = dClass.date
    o = dClass.open
    h = dClass.high
    l = dClass.low
    c = dClass.close
    v = dClass.volume
    oi = dClass.opInt
    r = dClass.range
    tr = dClass.trueRange
    return(d,o,h,l,c,v,oi,r,tr)

def getPortfolioOTE(marketMonitorList,numMarkets):
    bigOTELoser = -1;bigOTELoserNum = bigOTEWinner = bigOTEWinnerNum =0
    portIndividOTESum = 0
    if len(marketMonitorList) == numMarkets:
        oteString = ""
        for oteCnt in range(0,numMarkets):
            portIndividOTESum += marketMonitorList[oteCnt].ote
            oteString += str(round(marketMonitorList[oteCnt].ote,2)) + "  "
#            print(oteCnt," ",marketMonitorList[oteCnt].ote)
            if marketMonitorList[oteCnt].ote < bigOTELoser :
                bigOTELoser = marketMonitorList[oteCnt].ote
                bigOTELoserNum = oteCnt
            if marketMonitorList[oteCnt].ote > bigOTEWinner:
                bigOTEWinner = marketMonitorList[oteCnt].ote
                bigOTEWinnerNum = oteCnt
 #       print(oteString," ",portIndividOTESum)
        return (portIndividOTESum,bigOTEWinner,bigOTEWinnerNum,bigOTELoser,bigOTELoserNum)
def isNewMonth(dateList,curBar):
    if len(dateList)>curBar and curBar > 0:
        monthPriorDay = int(dateList[curBar-1]/100)%100
        monthToday = int(dateList[curBar]/100)%100
        if monthPriorDay != monthToday :
            return True
        else:
            return False
def isNewYear(dateList,curBar):
    if len(dateList)>curBar and curBar > 0:
        priorYear = int(dateList[curBar-1]/10000)%100
        thisYear = int(dateList[curBar]/10000)%100
        if priorYear != thisYear :
            return True
        else:
            return False


def getDOW(intDate):
    day = intDate % 100
    month = int(intDate/100)%100
    year = int(intDate/10000)
    dow = date(year, month, day).weekday()
    return dow



def getWeeklyData(marketData,numBarsBack,curBar):

    cnt = 0
    weekCnt = 0
    idx = curBar
    loop = True
    while (loop) :
        dow = getDOW(marketData.date[idx-cnt])
        dowYes =getDOW(marketData.date[idx-(cnt+1)])
        if dow < dowYes:
            if dow == 0 or dow == 1:
                weekCnt +=1
        if weekCnt > numBarsBack : loop = False
        cnt +=1
    dateW = list()
    openW = list()
    highW = list()
    lowW = list()
    closeW = list()
    rangeW = list()
    tRangeW = list()
    firstWeek = True
    hh = 0
    ll = 99999999
    weekCnt = 0
    cnt -=1
    for bars in range(curBar - cnt,curBar+1):
        if getDOW(marketData.date[bars]) < getDOW(marketData.date[bars-1]):
            weekCnt +=1
            if weekCnt > 1 : firstWeek = False
            if firstWeek == False:
                closeW.append(marketData.close[bars-1])
                highW.append(hh)
                lowW.append(ll)
                rangeW.append(hh-ll)
                tRangeW.append(max(closeW[-1],hh) - min(closeW[-1],ll))
                hh = 0
                ll = 99999999
            openW.append(marketData.open[bars])
            dateW.append(marketData.date[bars])
        hh = max(hh,marketData.high[bars])
        ll = min(ll,marketData.low [bars])
    #get current week high-low-close
    cnt = 1
    loop = True
    hh = marketData.high[curBar]
    ll = marketData.low[curBar]
    closeW.append(marketData.close[curBar])
    while (loop):
        curDow = getDOW(marketData.date[curBar])
        priorDow = getDOW(marketData.date[curBar-cnt])
        if curDow > priorDow and cnt < 5:
            hh = max(hh,marketData.high[curBar-cnt])
            ll = min(ll,marketData.low[curBar-cnt])
            cnt +=1
        else:
            loop = False
    highW.append(hh)
    lowW.append(ll)
    rangeW.append(hh-ll)
    tRangeW.append(max(closeW[-1],hh) - min(closeW[-1],ll))
    return dateW,openW,highW,lowW,closeW,rangeW,tRangeW







