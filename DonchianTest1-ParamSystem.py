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
#
#Code Refactor v001 by Anthony Kalomas
#
#- Identify/Isolate global variables
#- runDonchianSystem() - wraps backtesting into a runSystem function
#- exploreParameterSpace() - run backtests throughout the parameter space
#- createIntegerSequence() - create sequences for use with exploreParameterSpace()
#- To Do: continue breaking runDonchianSystem into smaller pieces
#--------------------------------------------------------------------------------
#Import Section - inlcude functions, classes, variables from external modules
#--------------------------------------------------------------------------------
# --- Do  not change below here
from getData import getData
from equityDataClass import equityClass
from tradeClass import tradeInfo
from systemMarket import systemMarketClass
from indicators import highest,lowest,rsiClass,stochClass,sAverage,bollingerBands

from portfolio import portfolioClass
from systemAnalytics import calcSystemResults
from utilityFunctions import getDataAtribs,getDataLists,roundToNearestTick,calcTodaysOTE
from utilityFunctions import setDataLists,removeDuplicates

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

#--------------------------------------------------------------------------------------------------------------------------
# - Helper function to create an ascending sequence of integers for optimizing
# - the result set includes both the start and the end of the sequence
# - if stepSize is too big, the list contains only the start and end values
# - if start and end are equal, the list contains only the start value
# - To Do: make a decimal version
#------------------------------------------------------------------------------------------------------------------------
def createIntegerSequence(start, end, stepSize):
    sequenceList = []
    #only allow positive stepSize
    stepSize = abs(stepSize)
    #swap start and end if start is greater than end
    if start > end:
        tempStart = start
        tempEnd = end
        start = tempEnd
        end = tempStart
    if start < end and stepSize < abs(end - start):
        for currentElement in range(start, end+stepSize, stepSize):
            sequenceList.append(currentElement)
    elif start < end and stepSize >= abs(end - start):
        sequenceList = [start, end]
    elif start == end:
        sequenceList = [start]
    #if we have gone past the end value remove it
    if len(sequenceList) > 2 and sequenceList[len(sequenceList)-1] > end:
        sequenceList.remove(sequenceList[len(sequenceList)-1])
    #include the end value in the series if we have not reached it
    if len(sequenceList) > 2 and sequenceList[len(sequenceList)-1] < end:
        sequenceList.append(end)
    return sequenceList


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
startTestDate = 20000101 #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'DonchTest-1' #System Name here
initCapital = 500000
commission = 50

#---------------------------------------------------------------------------------
# Do not change code below
#---------------------------------------------------------------------------------
dailyPortCombEqu = 0
curShares = 0

#
#
#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
#
#
sectorList = list()
sectorTradesTodayList = list()
numSectors = 7
#
myBPV=None;myComName=None;myMinMove=None

#--------------------------------------------------------------------------------------------------------------------------
# - wrap trading system into a "runSystem" function with input parameters
# - this allows us to easily test different combinations of system parameters
# - it also can allow us to switch reporting style and turn on/off live trading
# - I'm a big believer in live trading the exact same logic that has been tested ;)
# - we can also add other parameters that we think will be convenient to control
#------------------------------------------------------------------------------------------------------------------------
def runDonchianSystem(channelSlowLen=80,channelFastLen=20,atrLen=30,liveTrading=False,defaultReport=True):
#----------------------------------------------------------------------------------
# Reference global variables here
#----------------------------------------------------------------------------------
    global marketMonitorList,masterDateList,masterDateGlob,entryPrice,buy,entry,sell,exit,ignore
    global entryQuant,exitQuant,trueRanges,myBPVList,myComNameList,myMinMoveList,systemMarketList
    global cond1,cond2,cond3,cond4marketVal1,marketVal2,marketVal3,marketVal4
    global portManager,marketList,portfolio,numMarkets,positionMatrix,firstMarketLoop
    global startTestDate,stopTestDate,rampUp,sysName,initCapital,commission
    global dailyPortCombEqu, curShares
    global sectorList,sectorTradesTodayList,numSectors
    global mp,commission,totProfit,barsSinceEntry,listOfTrades
    global entryQuant,exitPrice,numShares,myBPV,cumuProfit,myComName,myMinMove
    global tradeName
#----------------------------------------------------------------------------------
# Initialize global variables to ensure we are starting fresh
# To Do: abstract initialization into a function
#----------------------------------------------------------------------------------
    print("Optimization: ",channelSlowLen," ",channelFastLen," ",atrLen)
    marketMonitorList,masterDateList,masterDateGlob,entryPrice = ([] for i in range(4))
    buy = entry = 1; sell = exit = -1; ignore = 0;
    entryQuant,exitQuant,trueRanges,myBPVList = ([] for i in range(4))
    myComNameList,myMinMoveList,systemMarketList = ([] for i in range(3))
    cond1,cond2,cond3,cond4 = ([] for i in range(4))
    marketVal1,marketVal2,marketVal3,marketVal4 = ([] for i in range(4))
    portManager = portManagerClass()
# load the market data elsewhere
# possibly check if we have market data loaded before proceeding
#    marketList = getData();
    portfolio = portfolioClass()
    numMarkets = len(marketList);positionMatrix = positionMatrixClass();positionMatrix.numMarkets = numMarkets
    firstMarketLoop = True
    dailyPortCombEqu = 0
    curShares = 0
    for curMarket in range(0,numMarkets):
        systemMarkTracker = systemMarkTrackerClass()
        equity = equityClass()
        systemMarkTracker.setSysMarkTrackingData(marketList[curMarket])
        systemMarkTracker.setSysMarkTrackingEquity(equity)
        marketMonitorList.append(systemMarkTracker)
        myBPV,myComName,myComLongName,mymyMinMove= getDataAtribs(marketMonitorList[curMarket].marketData)
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
# To Do: possibly abstract this into a function
#---------------------------------------------------------------------------------
    sectorList = list()
    sectorTradesTodayList = list()
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
        sectorTradesTodayList.append(0)
    for i in range(0,len(sectorList)):
        if sectorList[i].sectMarket != []: print(sectorList[i].sectMarket)
#---------------------------------------------------------------------------------
# Do not change code below
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
 #       if curPortBar % 100 == 0 : print("Working on bar #: ",curPortBar)
        for curMarket in range(0,numMarkets):
            if curMarket == 0 : indivMktAccum = initCapital
            myDate,myOpen,myHigh,myLow,myClose,myVolume,myOpInt,myRange,myTrueRange = setDataLists(marketMonitorList[curMarket].marketData)
            equItm = marketMonitorList[curMarket].equItm
            equItm += 1
            myBPV = myBPVList[curMarket];myComName = myComNameList[curMarket];myMinMove = myMinMoveList[curMarket]
            if curMarket == 0 : sectorTradesTodayList = [0] * numSectors
            if myComName not in portManager.marketSymbols:
                portManager.marketSymbols.append(myComName)
                portManager.numConts.append(1)
            curShares = 0;todaysCTE = todaysOTE = 0;mktsToday = 0
#---------------------------------------------------------------------------------
# Do not change code above
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
# Do not change code below
#---------------------------------------------------------------------------------
            if masterDateList[curPortBar] in marketMonitorList[curMarket].marketData.date:
                curBar = marketMonitorList[curMarket].marketData.date.index(masterDateList[curPortBar])
#                print("Current Pos Matrix ",myDate[curBar]," ",positionMatrix.posMatrixSize[-numMarkets:])
                yesterdaySectorPositions = numPosCurrentSector(sectorList,myComName,myComNameList,positionMatrix.posMatrixSize[-numMarkets:])
                curSector = getCurrentSector(myComName,sectorList)
                sectorPositions = yesterdaySectorPositions + sectorTradesTodayList[curSector]
#                print(myComName," ",curSector," ",sectorPositions);
#                print(myComName," ",numSectorPositions)
#                numSectorPositions = 0
                mp = 0
                if len(marketMonitorList[curMarket].mp)!=0: mp = marketMonitorList[curMarket].mp[-1]
                entryPrice = marketMonitorList[curMarket].entryPrice
                entryQuant= marketMonitorList[curMarket].entryQuant
                curShares = marketMonitorList[curMarket].curShares
                cumuProfit = marketMonitorList[curMarket].cumuProfit
                barsSinceEntry = marketMonitorList[curMarket].barsSinceEntry
#---------------------------------------------------------------------------------------------------
#  Start programming your great trading ideas below here - don't touch stuff above
#---------------------------------------------------------------------------------------------------
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
                buyLevel = highest(myHigh,channelSlowLen,curBar,1)
                shortLevel = lowest(myLow,channelSlowLen,curBar,1)
                longExit = lowest(myLow,channelFastLen,curBar,1)
                shortExit = highest(myHigh,channelFastLen,curBar,1)
                ATR = sAverage(myTrueRange,atrLen,curBar,1)
#                ATR = sAverage(myTrueRange,atrLen,curBar,1)
#                posSize = .005*dailyPortCombEqu/(ATR*myBPV)
#                print(myDate[curBar]," ",dailyPortCombEqu," ",.005*dailyPortCombEqu," ",ATR*myBPV)
#                posSize = int(posSize)
#                posSize = max(posSize,1)
                posSize = 1
                if mp != 0 : sectorPositions -= 1
#  Long Entry
#  Okay  Let's put in some logic to create a long position
                if myHigh[curBar] >= buyLevel and mp !=1:
                    price = max(myOpen[curBar],buyLevel)
                    if mp == 0 : sectorTradesTodayList[curSector] +=1
                    tradeName = "Simple Buy"
                    numShares = posSize
                    if mp <= -1:
                        profit,curShares,trades = bookTrade(-1,0,price,myDate[curBar],"RevshrtLiq",curShares)
                        marketMonitorList[curMarket].tradesList.append(trades);todaysCTE = profit
                    profit,curShares,trades = bookTrade(entry,buy,price,myDate[curBar],tradeName,numShares)
                    barsSinceEntry = 1
                    marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)
#  Long Exit
                if mp == 1 and myLow[curBar] <= longExit and barsSinceEntry > 1:
                    price = min(myOpen[curBar],longExit)
                    sectorTradesTodayList[curSector] -=1
                    tradeName = "Lxit"
                    numShares = curShares
                    profit,curShares,trades = bookTrade(exit,ignore,price,myDate[curBar],tradeName,numShares)
                    todaysCTE = profit;barsSinceEntry = 0
                    marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)
#  Short Entry
#  Okay  Let's put in some logic to create a short position
                if myLow[curBar] <= shortLevel and mp !=-1 :
                    price = min(myOpen[curBar],shortLevel)
                    if mp == 0 : sectorTradesTodayList[curSector] +=1
                    tradeName = "Simple Sell"
                    numShares = posSize
                    if mp >= 1:
                        profit,curShares,trades = bookTrade(-1,0,price,myDate[curBar],"RevLongLiq",curShares)
                        marketMonitorList[curMarket].tradesList.append(trades);todaysCTE = profit
                    profit,curShares,trades = bookTrade(entry,sell,price,myDate[curBar],tradeName,numShares)
                    barsSinceEntry = 1
                    marketMonitorList[curMarket].setSysMarkTrackingInfo(tradeName,cumuProfit,mp,barsSinceEntry,curShares,trades)
#  Short Exit
                if mp == -1 and myHigh[curBar] >= shortExit and barsSinceEntry > 1:
                    price = max(myOpen[curBar],shortExit)
                    sectorTradesTodayList[curSector] -= 1
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
#    sectors.setSectorsInfo(numSectors,systemMarketList)
    positionMatrix.printPositionMatrix(systemMarketList,portManager)
    portfolio.setPortfolioInfo("PortfolioTest",systemMarketList)
    parseSectors(sectorList,systemMarketList)
#    plotEquityCurve(portfolio)
#    calcSystemResults(systemMarketList)
#    logic to toggle between default reporting and parameter optimization style reporting
    if defaultReport==True:
        calcSystemResults(systemMarketList)
    else:
#       make parameter lists to conveniently pass to reporting function
        paramNames = [ "channelSlowLen","channelFastLen","atrLen" ]
        params = [ channelSlowLen, channelFastLen, atrLen]
#        calcStrategyOptimizationReport(systemMarketList, paramNames,params)
#---------------------------------------------------------------------------
#       To Do: implement calcStrategyOptimizationReport() function
#       generates a report like TradeStation's Strategy optimization Report
#       append single line system report to a text file for each parameter combo
#       report contains parameter settings and corresponding system summary stats for further analysis
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
# - now that we have defined a runSystem() function
# - we can run the system with default parameters by executing: runDonchianSystem()
# - or we can conveniently pass in other parameter combos as we explore the parameter space
#------------------------------------------------------------------------------------------------------------------------
#runDonchianSystem()
#runDonchianSystem(channelSlowLen=60,channelFastLen=25,atrLen=45,liveTrading=False,defaultReport=True)
#--------------------------------------------------------------------------------------------------------------------------
# - exploreParameterSpace()
# - generate sequences to step through parameter values
# - nested loops allow us to explore all parameter combos
# - for the donchian system we only sequences of integers
#------------------------------------------------------------------------------------------------------------------------
def exploreParameterSpace(slowLenStart=50,slowLenStop=100,slowLenStep=5,fastLenStart=15,fastLenStop=30, fastLenStep=1, atrLenStart=20,atrLenStop=50,atrLenStep=2):
    slowLenSequence=createIntegerSequence(slowLenStart, slowLenStop, slowLenStep)
    fastLenSequence=createIntegerSequence(fastLenStart, fastLenStop, fastLenStep)
    atrLenSequence=createIntegerSequence(atrLenStart, atrLenStop, atrLenStep)
#--------------------------------------------------------------------------------------------------------------------------
# - test all combinations of parameter values
#------------------------------------------------------------------------------------------------------------------------
    for mySlowLen in slowLenSequence:
        for myFastLen in fastLenSequence:
            for myAtrLen in atrLenSequence:
                runDonchianSystem(channelSlowLen=mySlowLen, channelFastLen=myFastLen, atrLen=myAtrLen, defaultReport=False)

exploreParameterSpace(slowLenStart=40,slowLenStop=100,slowLenStep=20,fastLenStart=15,fastLenStop=30, fastLenStep=5, atrLenStart=20,atrLenStop=20,atrLenStep=10)