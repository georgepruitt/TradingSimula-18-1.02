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
from getData import getData
from equityDataClass import equityClass
from tradeClass import tradeInfo
from systemMarket import systemMarketClass
from indicators import highest,highest2,lowest,lowest2,\
    rsiClass,stochClass,sAverage,bollingerBands
from portfolio import portfolioClass
from systemAnalytics import calcSystemResults
from utilityFunctions import getDataAtribs,getDataLists,roundToNearestTick,calcTodaysOTE
from utilityFunctions import setDataLists,removeDuplicates,calcAvgLongShort,isNewMonth,crosses
from utilityFunctions import getDOW, getWeeklyData
from portManager import portManagerClass,systemMarkTrackerClass
from positionMatrixClass import positionMatrixClass
from barCountCalc import barCountCalc

from sectorClass import sectorClass, parseSectors, numPosCurrentSector
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
myComNameList,myMinMoveList,systemMarketList = ([] for i in range(3))
cond1,cond2,cond3,cond4 = ([] for i in range(4))
marketVal1,marketVal2,marketVal3,marketVal4 = ([] for i in range(4))
portManager = portManagerClass();marketList = getData();portfolio = portfolioClass()
numMarkets = len(marketList);positionMatrix = positionMatrixClass();positionMatrix.numMarkets = numMarkets
curTradesList = list()
begOfMonthPortEqu =0
canTrade = True

#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = 20100112 #must be in yyyymmdd
stopTestDate = 20190228 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'TF-HHLL4-LLHH2' #System Name here
initCapital = 500000
commission = 50
#------ initiate algo specific variables here
portfolioClsTrdEqu = portfolioOTEEqu = 0

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
    myBPV,myComName,myMinMove= getDataAtribs(marketMonitorList[curMarket].marketData)
    myBPVList.append(myBPV);myComNameList.append(myComName);myMinMoveList.append(myMinMove)
    cond1.append(0);cond2.append(0);cond3.append(0),cond4.append(0)
    marketVal1.append(0);marketVal2.append(0);marketVal3.append(0),marketVal4.append(0)


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
        curTradesList = marketMonitorList[curMarket].tradesList
        myDate,myOpen,myHigh,myLow,myClose,myVolume,myOpInt,myRange,myTrueRange = setDataLists(marketMonitorList[curMarket].marketData)
        equItm = marketMonitorList[curMarket].equItm
        equItm += 1
        myBPV = myBPVList[curMarket];myComName = myComNameList[curMarket];myMinMove = myMinMoveList[curMarket]
        if myComName not in portManager.marketSymbols:
            portManager.marketSymbols.append(myComName)
            portManager.numConts.append(1)

        curShares = 0;todaysCTE = todaysOTE = 0;mktsToday = 0

        if masterDateList[curPortBar] in marketMonitorList[curMarket].marketData.date:
            curBar = marketMonitorList[curMarket].marketData.date.index(masterDateList[curPortBar])
            newMonth = isNewMonth(masterDateList,curPortBar)
            if canTrade == True and curMarket == 0:
                portfolioClsTrdEqu = portfolioOTEEqu =  0
                for tempCurMarket in range(0,numMarkets):
                    oteList = marketMonitorList[tempCurMarket].equity.openTrdEquity
                    portfolioClsTrdEqu += marketMonitorList[tempCurMarket].equity.cumuClsEquity
                    if len(oteList)>0 :
                        portfolioOTEEqu += oteList[-1]
            if newMonth:
                begOfMonthPortEqu = portfolioClsTrdEqu + portfolioOTEEqu
            canTrade = True
            if portfolioClsTrdEqu + portfolioOTEEqu < begOfMonthPortEqu - 5000:
                canTrade = False
#                print(myDate[curBar]," tuning off ",portfolioClsTrdEqu + portfolioOTEEqu," ",begOfMonthPortEqu)
#            numSectorPositions = numPosCurrentSector(sectorList,myComName,myComNameList,positionMatrix.posMatrixSize[-numMarkets:])
#            print(myDate[curBar]," ",myComName," ",portfolioOTEEqu," ",portfolioClsTrdEqu)
            numSectorPositions = 0

            mp = 0
            if len(marketMonitorList[curMarket].mp)!=0: mp = marketMonitorList[curMarket].mp[-1]
            entryPrice = marketMonitorList[curMarket].entryPrice
            entryQuant= marketMonitorList[curMarket].entryQuant
            curShares = marketMonitorList[curMarket].curShares
            cumuProfit = marketMonitorList[curMarket].cumuProfit
            barsSinceEntry = marketMonitorList[curMarket].barsSinceEntry

#            print(myDate[curBar]," ",cumuProfit," ",marketVal2[curMarket])

#---------------------------------------------------------------------------------------------------
#  Get average win and loss last 10 trades
#---------------------------------------------------------------------------------------------------
            dateW,openW,highW,lowW,closeW = getWeeklyData(marketMonitorList[curMarket].marketData,6,curBar)
#            weekOffset = 1
#            if getDOW(myDate[curBar]) < 4 : weekOffSet =-2
#            avgLong,avgShort,numLong,numShort = calcAvgLongShort(curTradesList,10)
#            print(masterDateList[curPortBar]," ",avgLong," ",avgShort," ",numLong," ",numShort)
#---------------------------------------------------------------------------------------------------
#  Start programming your great trading ideas below here - don't touch stuff above
#---------------------------------------------------------------------------------------------------
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations

            upBand,dnBand, midBand = bollingerBands(myDate,myClose,80,2,curBar,1)
            buyLevel = roundToNearestTick(upBand,1,myMinMove)
            shortLevel =roundToNearestTick(dnBand,-1,myMinMove)
            longExit = roundToNearestTick(midBand,-1,myMinMove)
            shortExit = roundToNearestTick(midBand,1,myMinMove)

            hh_1 = highest(myHigh,20,curBar,1)
            hh_4 = highest2(highW,4,2)
            ll_4 = lowest2(lowW,4,2)
            hh_2 = highest2(highW,2,2)
            ll_2 = lowest2(lowW,2,2)

   #         print(myDate[curBar]," ",hh_1," ",hh_2," ",highW[-1]," ",highW[-2]," ",highW[-3]," ",highW[-4]," ",highW[-5]," ",len(highW))

            ATR = sAverage(myTrueRange,30,curBar,1)

            posSize = .005*dailyPortCombEqu/(ATR*myBPV)
 #           print(myDate[curBar]," ",dailyPortCombEqu," ",.005*dailyPortCombEqu," ",ATR*myBPV)
            posSize = int(posSize)
            posSize = max(posSize,1)
            posSize = 1
#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if crosses(myClose,hh_2,1,curBar-1) and mp !=1 :
                price = myOpen[curBar]
                tradeName = "HH4CrossB"
                numShares = posSize
                if mp <= -1:
                    profit,curShares,trades = bookTrade(-1,0,price,myDate[curBar],"RevshrtLiq",curShares)
                    marketMonitorList[curMarket].tradesList.append(trades);todaysCTE = profit
                profit,curShares,trades = bookTrade(entry,buy,price,myDate[curBar],tradeName,numShares)
                barsSinceEntry = 1
                marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)
#  Long Exit
            if mp == 1 and myClose[curBar-1] <= ll_2 and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Lxit"
                numShares = curShares
                profit,curShares,trades = bookTrade(exit,ignore,price,myDate[curBar],tradeName,numShares)
                todaysCTE = profit;barsSinceEntry = 0
                marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)


#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if crosses(myClose,ll_4,-1,curBar-1) and mp !=-1 :
                price = myOpen[curBar]
                if mp >= 1:
                    profit,curShares,trades = bookTrade(-1,0,price,myDate[curBar],"RevLongLiq",curShares)
                    marketMonitorList[curMarket].tradesList.append(trades);todaysCTE = profit
                tradeName = "LL4CrossS";numShares = posSize
                profit,curShares,trades = bookTrade(entry,sell,price,myDate[curBar],tradeName,numShares)
                barsSinceEntry = 1
                marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)
#  Short Exit
            if mp == -1 and myClose[curBar-1] >= hh_2 and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Sxit"
                numShares = curShares
                profit,curShares,trades = bookTrade(exit,ignore,price,myDate[curBar],tradeName,numShares)
                todaysCTE = profit;barsSinceEntry = 0
                marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)


#----------------------------------------------------------------------------------------------------------------------------
# - Do not change code below - trade, portfolio accounting - our great idea should stop here
#----------------------------------------------------------------------------------------------------------------------------
            if mp != 0 :
                barsSinceEntry += 1
                todaysOTE = calcTodaysOTE(mp,marketList[curMarket].close[curBar],marketMonitorList[curMarket].entryPrice,marketMonitorList[curMarket].entryQuant,myBPV)
            marketMonitorList[curMarket].barsSinceEntry = barsSinceEntry
            marketMonitorList[curMarket].curShares = curShares
            marketMonitorList[curMarket].equItm = equItm
            marketMonitorList[curMarket].ote = todaysOTE
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
    dailyPortCombEqu = indivMktAccum
    portManager.combinedEquity.append(dailyPortCombEqu)
    positionMatrix.posMatrixDate.append(masterDateList[curPortBar])
    for mktCnt in range(0,len(marketMonitorList)):
        positionMatrix.posMatrixSize.append(marketMonitorList[mktCnt].curShares)
cnt = 0
for j in range(0,numMarkets):
    systemMarket = systemMarketClass()
    systemMarket.setSysMarkInfo(sysName,myComNameList[j],marketMonitorList[j].tradesList,marketMonitorList[j].equity,initCapital)
    systemMarketList.append(systemMarket)
#sectors.setSectorsInfo(numSectors,systemMarketList)
positionMatrix.printPositionMatrix(systemMarketList,portManager)
portfolio.setPortfolioInfo("PortfolioTest",systemMarketList)
parseSectors(sectorList,systemMarketList)
#plotEquityCurve(portfolio)
calcSystemResults(systemMarketList)
