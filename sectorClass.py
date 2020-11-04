import operator

class sectorClass(object):
    def __init__(self):
        self.sectName = ""
        self.sectMarket = list()
        self.sectSysMarket = list()

    def assignSectors(self,sectorName,symbolsString,symbolList):
        self.sectName = sectorName
        for chars in range(0,len(symbolsString)):
            if symbolsString[2*chars:2*chars+2] in symbolList:
                self.sectMarket.append(symbolsString[2*chars:2*chars+2])


def numPosCurrentSector(sectorList,curMarket,symbolList,positionList):
    for sector in range(0,len(sectorList)):
        whichSector = -1
        if curMarket in sectorList[sector].sectMarket:
            whichSector = sector
            break
    numSectorPos = 0
    if whichSector != -1:
        for sectorMarkets in range (0,len(sectorList[whichSector].sectMarket)):
            for symbols in range(0,len(symbolList)):
                tempMarket1 = sectorList[whichSector].sectMarket[sectorMarkets]
                tempMarket2 = symbolList[symbols]
                if tempMarket1 == tempMarket2:
                    if positionList != []:
                        curMktPos = symbols - len(symbolList)
                        if positionList[curMktPos] > 0:
                            numSectorPos +=1
    return(numSectorPos)

def getCurrentSector(curMarket,sectorList):
    for sector in range(0,len(sectorList)):
        whichSector = -1
        if curMarket in sectorList[sector].sectMarket:
            whichSector = sector
            break
    return(whichSector)

def parseSectors(sectorList,systemMarketList):
    masterDateList = list()
    pEquityTuple = list()
    combinedEquity = list()
    begDate = 99999999
    endDate = 0

    fileName1 = systemMarketList[0].systemName + "-Sectors.txt"
    target1 = open(fileName1,"w")

    for numSect in range(0,len(sectorList)):
        for numSysMarket in range(0,len(systemMarketList)):
            if systemMarketList[numSysMarket].symbol in sectorList[numSect].sectMarket:
#                    print(sectorList[numSect].sectName," ",systemMarketList[numSysMarket].symbol," ",systemMarketList[numSysMarket].profitLoss)
                 sectorList[numSect].sectSysMarket.append(systemMarketList[numSysMarket])
    for numSect in range(0,len(sectorList)):
        if sectorList[numSect].sectSysMarket != []:
            masterDateList[:] = []
            pEquityTuple[:] = []
            portPeakEquity = -999999999999
            portMinEquity = -999999999999
            portPeakEquity = -999999999999
            portMinEquity = -999999999999
            portMaxDD = 0
            lineOutPut = sectorList[numSect].sectName + "     -------------------------------"
            target1.write('%-10s --------------------\n' % sectorList[numSect].sectName)
       #     target1.write(lineOutPut)
       #     target1.write("\n")
            print('%-10s ' % (sectorList[numSect].sectName),"-------------------------------")
            for numSysMarket in range(0,len(sectorList[numSect].sectSysMarket)):
                print('%-8s %10.0f %10.0f ' % (sectorList[numSect].sectSysMarket[numSysMarket].symbol,sectorList[numSect].sectSysMarket[numSysMarket].profitLoss,
                sectorList[numSect].sectSysMarket[numSysMarket].maxxDD))
                target1.write('%-8s %10.0f %10.0f \n' % (sectorList[numSect].sectSysMarket[numSysMarket].symbol,sectorList[numSect].sectSysMarket[numSysMarket].profitLoss,
                sectorList[numSect].sectSysMarket[numSysMarket].maxxDD))
       #         lineOutPut = ""
       #         lineOutPut = sectorList[numSect].sectSysMarket[numSysMarket].symbol + "      " + str(round((sectorList[numSect].sectSysMarket[numSysMarket].profitLoss),2)) +  "  " +str(round((sectorList[numSect].sectSysMarket[numSysMarket].maxxDD),2))
       #         target1.write(lineOutPut)
       #         target1.write("\n")
                masterDateList += sectorList[numSect].sectSysMarket[numSysMarket].equity.equityDate
            masterDateList = removeDuplicates(masterDateList)
            masterDateList = sorted(masterDateList)
            lineOutPut = "-------------------------------------------"
            target1.write(lineOutPut)
            target1.write("\n")
            print("-------------------------------------------")
            priorIdxlist = list()
            priorIdxList = [0] * len(sectorList)
            for i in range(0,len(masterDateList)):
                cumuVal = 0
                for j in range(0,len(sectorList[numSect].sectSysMarket)):
                    skipDay = 0
                    try:
                        idx = sectorList[numSect].sectSysMarket[j].equity.equityDate.index(masterDateList[i])
                    except ValueError:
                        skipDay = 1
                        marketDayCumu = 0
                        skipDate = masterDateList[i]
                        skipMkt = sectorList[numSect].sectSysMarket[j].symbol
                        numDaysInEquityStream = len(sectorList[numSect].sectSysMarket[j].equity.dailyEquityVal)
                        marketBeginDate = sectorList[numSect].sectSysMarket[j].equity.equityDate[0]
                        if (masterDateList[i] > marketBeginDate and i < numDaysInEquityStream):
                            marketDayCumu = sectorList[numSect].sectSysMarket[j].equity.dailyEquityVal[priorIdxList[j]]
                        else:
                            if masterDateList[i] < marketBeginDate:
                                marketDayCumu = 0
                            else:
                                marketDayCumu = sectorList[numSect].sectSysMarket[j].equity.dailyEquityVal[-1]
                        pEquityTuple += ((i,j,marketDayCumu),)
                        cumuVal += marketDayCumu
                    if skipDay == 0:
                        priorIdxList[j] = idx
                        marketDayCumu = sectorList[numSect].sectSysMarket[j].equity.dailyEquityVal[idx]
                        pEquityTuple += ((i,j,marketDayCumu),)
                        cumuVal += sectorList[numSect].sectSysMarket[j].equity.dailyEquityVal[idx]
                combinedEquity.append(cumuVal)
                if cumuVal > portPeakEquity: portPeakEquity = cumuVal
                portMinEquity = max(portMinEquity,portPeakEquity - cumuVal)
                portMaxDD = portMinEquity
##            lineOutPut = "Totals: " + str(round(cumuVal,0)) + " " + str(round(portMaxDD,0))
##            target1.write(lineOutPut)
##            target1.write("\n")
##            target1.write("-------------------------------------------")
##            target1.write("\n")
            target1.write('%-8s %10.0f %10.0f \n' % ("Totals: ",cumuVal,portMaxDD))
            target1.write("-------------------------------------------\n")
            print("Totals: ",'%10.0f %10.0f' % (cumuVal,portMaxDD))
            print("-------------------------------------------")

def sortRiskPerSector(myComNameList,sectorList,longRisk,shortRisk,maxPerSector,upOrDn):
    canBuyList = list()
    canShortList = list()
    sectMarketRisk = list()
    for cnt in range(0,len(myComNameList)):
        curSect = getCurrentSector(myComNameList[cnt],sectorList)
        sectMarketRisk.append((curSect,cnt,longRisk[cnt],shortRisk[cnt]))
        canBuyList.append(99999)
        canShortList.append(99999)

    sectMarketLongRisk = sectMarketRisk.copy()
    sectMarketShortRisk = sectMarketRisk.copy()
    sortOrder = False
    if upOrDn == -1: sortOrder = True
    sectMarketLongRisk.sort(key=operator.itemgetter(0,2),reverse = sortOrder)
    sectMarketShortRisk.sort(key=operator.itemgetter(0,3),reverse = sortOrder)
    for j in range(0,len(sectorList)):
        lsectCnt = 0
        for i in range(0,len(sectMarketLongRisk)):
            if sectMarketLongRisk[i][0] == j:
                if lsectCnt < maxPerSector:
                    canBuyList[i] = sectMarketLongRisk[i][1]
                lsectCnt += 1

        ssectCnt = 0
        for i in range(0,len(sectMarketShortRisk)):
            if sectMarketShortRisk[i][0] == j:
                if ssectCnt < maxPerSector:
                    canShortList[i] = sectMarketShortRisk[i][1]
                ssectCnt += 1
    return(canBuyList,canShortList)



def removeDuplicates(li):
    my_set = set()
    res = []
    for e in li:
        if e not in my_set:
            res.append(e)
            my_set.add(e)
    return res


