#-------------------------------------------------------------------------------
# Name:        portManager
# Purpose:
#
# Author:      georg
#
# Created:     11/09/2018
# Copyright:   (c) georg 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from marketDataClass import marketDataClass
from equityDataClass import equityClass
from tradeClass import tradeInfo

class portManagerClass(object):
    def __init__(self):
        self.portDate = list()
        self.marketSymbols= list()
        self.individEquity = list()
        self.combinedEquity = list()
        self.numConts = list()

class systemMarkTrackerClass(object):
    def __init__(self):
        self.marketData = marketDataClass
        self.entryPrice = list()
        self.entryQuant = list()
        self.exitQuant = list()
        self.entryName =list()
        self.mp = list()
        self.curShares = 0
        self.tradesList = list()
        self.equity = equityClass
        self.totProfit = 0
        self.barsSinceEntry = 0
        self.maxContractProfit = 0
        self.cumuProfit = 0
        self.ote = 0
        self.equItm = 0
        self.userVar1 = 0
        self.userVar2 = 0
        self.userVar3 = 0
        self.userVar4 = 0
        self.userList1 = list()
        self.userList2 = list()
        self.userList3 = list()


    def setSysMarkTrackingData(self,marketData):
        self.marketData = marketData

    def setSysMarkTrackingInfo(self,entryName,cumuProfit,mp,barsSinceEntry,curShares,trades):
#        self.entryPrice = entryPrice
#        self.entryQuant = entryQuant
        self.entryName.append(entryName)
        self.mp.append(mp)
        self.cumuProfit = cumuProfit
        self.curShares = curShares
        self.barsSinceEntry = barsSinceEntry
        self.tradesList.append(trades)

    def setSysMarkTrackingEquity(self,equity):
        self.equity = equity

 #Created May 2020 - keeps track of max profit for current contract
    def calcMaxContractProfit(self,mp,maxConProf):
        if maxConProf == 0:
            self.maxContractProfit = maxConProf
        else:
            if maxConProf > self.maxContractProfit: self.maxContractProfit = maxConProf

def normalize(normDataList,posSizeList):
    maxNormVal = 0
    for i in range(0,len(normDataList)):
        maxNormVal = max(maxNormVal,normDataList[i])
  #  print("*****************")
    for i in range(0,len(normDataList)):
        if normDataList[i] > 0: posSizeList[i] = maxNormVal/normDataList[i]
        posSizeList[i] = int(posSizeList[i])
        posSizeList[i] = max(posSizeList[i],1)
 #       print(maxNormVal," ",normDataList[i]," ",posSizeList[i])
    return posSizeList