#--------------------------------------------------------------------------------
#   If you want to ignore a bunch of non-eseential stuff then
#      S C R O L L   A L M O S T  H A L F   W A Y  D O W N
#--------------------------------------------------------------------------------
#TradingSimula18.py - programmed by George Pruitt
#Built on the code and ideas from "The Ultimate Algorithmic Tradins System T-Box"
#Code is broken into sections
#Most sections can and should be ignored
#Each trading algorithm must be programmed with this template
#This is the main entry into the platform
#--------------------------------------------------------------------------------
#Import Section - inlcude functions, classes, variables from external modules
#--------------------------------------------------------------------------------
# --- Do  not change below here
from math import trunc
from getData import getData
from equityDataClass import equityClass
from tradeClass import tradeInfo
from systemMarket import systemMarketClass
from indicators import highest,lowest,rsiClass,stochClass,sAverage,bollingerBands,\
    adxClass,sAverage2,parabolicClass
from portfolio import portfolioClass
from systemAnalytics import calcSystemResults
from utilityFunctions import getDataAtribs,getDataLists,roundToNearestTick,calcTodaysOTE
from utilityFunctions import setDataLists,removeDuplicates,isNewMonth,crosses
from utilityFunctions import getWeeklyData
from portManager import portManagerClass,systemMarkTrackerClass
from positionMatrixClass import positionMatrixClass
from barCountCalc import barCountCalc

from sectorClass import sectorClass, parseSectors, numPosCurrentSector,getCurrentSector
#-------------------------------------------------------------------------------------------------
# Pay no attention to these two functions - unless you want to
#-------------------------------------------------------------------------------------------------
def exitPos(myExitPrice,myExitDate,tempName,myCurShares):
    global tradeName,entryPrice,entryQuant,exitPrice,numShares,myBPV,cumuProfit
    if mp < 0:
        trades = tradeInfo('liqShort',myExitDate,tempName,myExitPrice,myCurShares,0)
        profit = trades.calcTradeProfit('liqShort',mp,entryPrice,myExitPrice,entryQuant,myCurShares) * myBPV
        profit = profit - myCurShares *commission;trades.tradeProfit = profit;cumuProfit += profit
        trades.cumuProfit = cumuProfit
    if mp > 0:
        trades = tradeInfo('liqLong',myExitDate,tempName,myExitPrice,myCurShares,0)
        profit = trades.calcTradeProfit('liqLong',mp,entryPrice,myExitPrice,entryQuant,myCurShares) * myBPV
        profit = profit - myCurShares * commission;trades.tradeProfit = profit;cumuProfit += profit
        trades.cumuProfit = cumuProfit
    curShares = 0
    for remShares in range(0,len(entryQuant)):curShares += entryQuant[remShares]
    return (profit,trades,curShares)

def bookTrade(entryOrExit,lOrS,price,date,tradeName,shares):
    global mp,commission,totProfit,curShares,barsSinceEntry,listOfTrades
    global entryPrice,entryQuant,exitPrice,numShares,myBPV,cumuProfit
    if entryOrExit == -1:
        profit,trades,curShares = exitPos(price,date,tradeName,shares);mp = 0
    else:
        profit = 0;curShares = curShares + shares;barsSinceEntry = 1;entryPrice.append(price);entryQuant.append(shares)
        if lOrS == 1:mp += 1;trades = tradeInfo('buy',date,tradeName,entryPrice[-1],shares,1)
        if lOrS ==-1:mp -= 1;trades = tradeInfo('sell',date,tradeName,entryPrice[-1],shares,1)
    return(profit,curShares,trades)

dataClassList = list()

marketMonitorList,masterDateList,masterDateGlob,entryPrice = ([] for i in range(4))
buy = entry = 1; sell = exit = -1; ignore = 0;
entryQuant,exitQuant,trueRanges,myBPVList = ([] for i in range(4))
myComNameList,myComLongNameList,myMinMoveList,systemMarketList = ([] for i in range(4))
cond1,cond2,cond3,cond4 = ([] for i in range(4))
marketVal1,marketVal2,marketVal3,marketVal4 = ([] for i in range(4))
portManager = portManagerClass();marketList = getData();portfolio = portfolioClass()
numMarkets = len(marketList);positionMatrix = positionMatrixClass();positionMatrix.numMarkets = numMarkets
firstMarketLoop = True

#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate  = 99999999 #must be in yyyymmdd
rampUp = 200 # need this minimum of bars to calculate indicators
sysName = 'TF-System#5' #System Name here
initCapital = 500000
commission = 50


#---------------------------------------------------------------------------------
# Optional - use this area to create user lists and
#            lists of indicator classes - include the list in the loop
#            if you need to instantiate or initialize
#---------------------------------------------------------------------------------

longExit = shortExit = 0
afLimit = 0.20
afStep = 0.02

buyLevel = list()
shortLevel= list()
stopPrice = list()
AF = list()
for curMarket in range(0,numMarkets):
    buyLevel.append(9999999)
    shortLevel.append(0)
    AF.append(0.02)
    stopPrice.append(0)


#---------------------------------------------------------------------------------
# Do not change code below
#---------------------------------------------------------------------------------

dailyPortCombEqu = 0
curShares = 0
for curMarket in range(0,numMarkets):
    systemMarkTracker = systemMarkTrackerClass()
    equity = equityClass()
    systemMarkTracker.setSysMarkTrackingData(marketList[curMarket])
    systemMarkTracker.setSysMarkTrackingEquity(equity)
    marketMonitorList.append(systemMarkTracker)
    myBPV,myComName,myComLongName,myMinMove= getDataAtribs(marketMonitorList[curMarket].marketData)
    myBPVList.append(myBPV);myComNameList.append(myComName);myMinMoveList.append(myMinMove)
    myComLongNameList.append(myComLongName)
    cond1.append(1);cond2.append(1);cond3.append(1),cond4.append(1)
    marketVal1.append(0);marketVal2.append(0);marketVal3.append(0),marketVal4.append(0)
#---------------------------------------------------------------------------------
# Do not change code above
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Set Up Sectors Here - remember you must use the exact symbol for each marketData
# Review process in book if necessary
#---------------------------------------------------------------------------------
sectorList = list()
numSectors = 7
for sector in range(0,numSectors):
    sectors = sectorClass()
    if sector == 0 : sectors.assignSectors("Currency","BPSFADDXECJYCD",myComNameList)
    if sector == 1 : sectors.assignSectors("Energies","CLHONGRB",myComNameList)
    if sector == 2 : sectors.assignSectors("Metals","GCSIHGPLPA",myComNameList)
    if sector == 3 : sectors.assignSectors("Grains","S_W_C_BOSMRR",myComNameList)
    if sector == 4 : sectors.assignSectors("Financials","USTYTUFVED",myComNameList)
    if sector == 5 :  sectors.assignSectors("Softs","SBKCCCCTLBOJ",myComNameList)
    if sector == 6 :sectors.assignSectors("Meats","LCLHFC",myComNameList)
    sectorList.append(sectors)

for i in range(0,len(sectorList)):
    if sectorList[i].sectMarket != []: print(sectorList[i].sectMarket)

#---------------------------------------------------------------------------------
# Do not change code above
#---------------------------------------------------------------------------------
masterDateGlob = list()
for curMarket in range(0,numMarkets):
    numDaysInData = len(marketMonitorList[curMarket].marketData.date)
    masterDateGlob += marketMonitorList[curMarket].marketData.date
    positionMatrix.marketNames.append(myComNameList[curMarket])
masterDateList = removeDuplicates(masterDateGlob);masterDateList = sorted(masterDateList)
barCount, endBarCount = barCountCalc(masterDateList,startTestDate,stopTestDate,rampUp)
portEquItm = barsSinceEntry = 0;dailyPortCombEqu = initCapital
for curPortBar in range(barCount,endBarCount+1):
    portManager.portDate.append(masterDateList[curPortBar])
    if curPortBar % 225 == 0 : print("Working on bar #: ",curPortBar)
    for curMarket in range(0,numMarkets):
        if curMarket == 0 : indivMktAccum = initCapital
        myDate,myOpen,myHigh,myLow,myClose,myVolume,myOpInt,myRange,myTrueRange = setDataLists(marketMonitorList[curMarket].marketData)

        equItm = marketMonitorList[curMarket].equItm
        equItm += 1
        myBPV = myBPVList[curMarket];myComName = myComNameList[curMarket];myMinMove = myMinMoveList[curMarket]
#        print(myComName," first date ",myDate[0])
        if myComName not in portManager.marketSymbols:
            portManager.marketSymbols.append(myComName)
            portManager.numConts.append(1)
        curShares = 0;todaysCTE = todaysOTE = 0;mktsToday = 0
#---------------------------------------------------------------------------------
# Do not change code above
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#  Assign lists based on marketMonitor here - assigning temp lists here is great idea
#--------------------------------------------------------------------------------------------------
        curTradesList = marketMonitorList[curMarket].tradesList
#---------------------------------------------------------------------------------
# Do not change code above
#---------------------------------------------------------------------------------
#        print("$$$$$  ", masterDateList[curPortBar]," ",marketMonitorList[curMarket].marketData.date[0])
        if masterDateList[curPortBar] in marketMonitorList[curMarket].marketData.date:
            curBar = marketMonitorList[curMarket].marketData.date.index(masterDateList[curPortBar])
            if curBar <= rampUp: continue
#            print ("Found : ",masterDateList[curPortBar])
#           print("Current Pos Matrix ",myDate[curBar]," ",positionMatrix.posMatrixSize[-numMarkets:])
            numSectorPositions = numPosCurrentSector(sectorList,myComName,myComNameList,positionMatrix.posMatrixSize[-numMarkets:])
#           print(myComName," ",numSectorPositions)
            numSectorPositions = 0
            mp = 0
            if len(marketMonitorList[curMarket].mp)!=0: mp = marketMonitorList[curMarket].mp[-1]
            entryPrice = marketMonitorList[curMarket].entryPrice
            entryQuant= marketMonitorList[curMarket].entryQuant
            curShares = marketMonitorList[curMarket].curShares
            cumuProfit = marketMonitorList[curMarket].cumuProfit
            barsSinceEntry = marketMonitorList[curMarket].barsSinceEntry

#---------------------------------------------------------------------------------
# Do not change code above
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
#  Preprocessing prior to the first market of the day is done here
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
#  Start programming your great trading ideas below here - don't touch stuff above
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#  Remember every line of code is executed on every day of every market#
#  Make sure you want to do this - if not it can slow down processing
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations


            buyLevel,shortLevel,midBand = bollingerBands(myDate,myClose,80,2,curBar,1)
            buyLevel = roundToNearestTick(buyLevel,1,myMinMove)
            shortLevel = roundToNearestTick(shortLevel,-1,myMinMove)
            if mp == 1 :
                if barsSinceEntry == 2:
                    stopPrice[curMarket] = myLow[curBar-1] - sAverage(myTrueRange,10,curBar-1,1)* 2
                    AF[curMarket] = afStep
                    marketVal1[curMarket] = myHigh[curBar-1]
                else:
                    newHigh = False
                    if myHigh[curBar-1] > marketVal1[curMarket]:
                        marketVal1[curMarket] = myHigh[curBar-1]
                        newHigh = True
                    stopPrice[curMarket] = stopPrice[curMarket]+ AF[curMarket] * (marketVal1[curMarket] - stopPrice[curMarket])
                    if newHigh and AF[curMarket] <afLimit:
                        AF[curMarket] = AF[curMarket] + min(afStep,afLimit- AF[curMarket])
                if stopPrice[curMarket] > myLow[curBar-1]:
                    stopPrice[curMarket] =myLow[curBar-1]
                print(myDate[curBar]," ",stopPrice[curMarket]," ",marketVal1[curMarket]," ",AF[curMarket])
            if mp ==-1 :
                if barsSinceEntry == 2:
                    stopPrice[curMarket] = myHigh[curBar-1] + sAverage(myTrueRange,10,curBar-1,1)* 2
                    AF[curMarket] = afStep
                    marketVal2[curMarket] = myLow[curBar-1]
                else:
                    newLow = False
                    if myLow[curBar-1] < marketVal2[curMarket]:
                        marketVal2[curMarket] = myLow[curBar-1]
                        newLow = True
                    stopPrice[curMarket] = stopPrice[curMarket]- AF[curMarket] * (stopPrice[curMarket]-marketVal2[curMarket])
                    if newLow and AF[curMarket] <afLimit:
                        AF[curMarket] = AF[curMarket] + min(afStep,afLimit- AF[curMarket])
                if stopPrice[curMarket] < myHigh[curBar-1]:
                    stopPrice[curMarket] =myHigh[curBar-1]
            posSize = 1

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if  myHigh[curBar] >= buyLevel and mp !=1 :
                price = max(myOpen[curBar],buyLevel)
                tradeName = "TF_Sys5:B"
                numShares = posSize
                if mp <= -1:
                    profit,curShares,trades = bookTrade(-1,0,price,myDate[curBar],"RevshrtLiq",curShares)
                    marketMonitorList[curMarket].tradesList.append(trades);todaysCTE = profit
                profit,curShares,trades = bookTrade(entry,buy,price,myDate[curBar],tradeName,numShares)
                barsSinceEntry = 1
                marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)
#  Long Exit
            if mp == 1 and myLow[curBar] <= stopPrice[curMarket] and barsSinceEntry > 1:
                price = min(myOpen[curBar],stopPrice[curMarket])
                tradeName = "Lxit1"
                numShares = curShares
                profit,curShares,trades = bookTrade(exit,ignore,price,myDate[curBar],tradeName,numShares)
                todaysCTE = profit;barsSinceEntry = 0
                marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)


#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if myLow[curBar] <= shortLevel and mp !=-1:
                price = min(myOpen[curBar],shortLevel)
                tradeName = "TF_Sys4:S"
                numShares = posSize
                if mp >= 1:
                    profit,curShares,trades = bookTrade(-1,0,price,myDate[curBar],"RevLongLiq",curShares)
                    marketMonitorList[curMarket].tradesList.append(trades);todaysCTE = profit
                profit,curShares,trades = bookTrade(entry,sell,price,myDate[curBar],tradeName,numShares)
                barsSinceEntry = 1
                marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)
#  Short Exit

            if mp == -1 and myHigh[curBar] >= stopPrice[curMarket] and barsSinceEntry > 1:
                price = max(myOpen[curBar],stopPrice[curMarket])
                tradeName = "Sxit"
                numShares = curShares
                profit,curShares,trades = bookTrade(exit,ignore,price,myDate[curBar],tradeName,numShares)
                todaysCTE = profit;barsSinceEntry = 0
                marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)



#----------------------------------------------------------------------------------------------------------------------------
# - Do not change code below - trade, portfolio accounting - our great idea should stop here
#----------------------------------------------------------------------------------------------------------------------------
            if mp != 0 :barsSinceEntry += 1;todaysOTE = calcTodaysOTE(mp,marketList[curMarket].close[curBar],marketMonitorList[curMarket].entryPrice,marketMonitorList[curMarket].entryQuant,myBPV)
            marketMonitorList[curMarket].barsSinceEntry = barsSinceEntry
            marketMonitorList[curMarket].curShares = curShares
            marketMonitorList[curMarket].equItm = equItm
            marketMonitorList[curMarket].equity.setEquityInfo(marketList[curMarket].date[curBar],equItm,todaysCTE,todaysOTE)
            portManager.individEquity.append((curMarket,marketMonitorList[curMarket].equity.dailyEquityVal[-1]))
            indivMktAccum += portManager.individEquity[portEquItm][1]
            portEquItm += 1
            if curPortBar == endBarCount:
                if mp >= 1:
                    price = marketList[curMarket].close[curBar]
                    exitDate = marketList[curMarket].date[curBar]
                    profit,trades,curShares = exitPos(price,marketList[curMarket].date[curBar],"L-EOD",curShares)
                    marketMonitorList[curMarket].tradesList.append(trades)
                if mp <= -1:
                    price = marketList[curMarket].close[curBar]
                    exitDate = marketList[curMarket].date[curBar]
                    profit,trades,curShares = exitPos(price,marketList[curMarket].date[curBar],"S-EOD",curShares)
                    marketMonitorList[curMarket].tradesList.append(trades)
        else:
            equityStreamLen = len(marketMonitorList[curMarket].equity.dailyEquityVal)
            if equityStreamLen > 0: portManager.individEquity.append((curMarket,marketMonitorList[curMarket].equity.dailyEquityVal[-1]))
            else: portManager.individEquity.append((curMarket,0.0))
            indivMktAccum += portManager.individEquity[portEquItm][1]
            portEquItm += 1
    if curMarket == numMarkets - 1 and firstMarketLoop == True: firstMarketLoop = False
    dailyPortCombEqu = indivMktAccum
    portManager.combinedEquity.append(dailyPortCombEqu)
    positionMatrix.posMatrixDate.append(masterDateList[curPortBar])
    for mktCnt in range(0,len(marketMonitorList)):
        positionMatrix.posMatrixSize.append(marketMonitorList[mktCnt].curShares)
cnt = 0
for j in range(0,numMarkets):
    systemMarket = systemMarketClass()
    systemMarket.setSysMarkInfo(sysName,myComNameList[j],myComLongNameList[j],marketMonitorList[j].tradesList,marketMonitorList[j].equity,initCapital)
    systemMarketList.append(systemMarket)
#sectors.setSectorsInfo(numSectors,systemMarketList)
positionMatrix.printPositionMatrix(systemMarketList,portManager)
portfolio.setPortfolioInfo("PortfolioTest",systemMarketList)
parseSectors(sectorList,systemMarketList)
#plotEquityCurve(portfolio)
calcSystemResults(systemMarketList)
