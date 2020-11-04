from math import atan
from math import degrees


class parabolicClass(object):
    def __init__(self):
        self.parOp =0
        self.parCl = 0
        self.position =0
        self.tradeHH = list()
        self.tradeLL = list()
        self.af = 0
        self.transition = 0
        self.seed= 0

    def calcParabolic(self,hPrices,lPrices,afStep,afLimit,curBar,offset):
        curBarLookBack = curBar - offset
        if self.seed == 0:
            self.parOp = hPrices[curBarLookBack] ;
            self.position = -1 ;
            self.tradeHH.append(hPrices[curBarLookBack])
            self.tradeLL.append(lPrices[curBarLookBack])
            self.af = afStep

        self.transition = 0
        self.seed = 1

        if hPrices[curBarLookBack] > self.tradeHH[-1]:
            self.tradeHH.append(hPrices[curBarLookBack])
        else:
            self.tradeHH.append(self.tradeHH[-1])

        if lPrices[curBarLookBack] < self.tradeLL[-1]:
            self.tradeLL.append(lPrices[curBarLookBack])
        else:
            self.tradeLL.append(self.tradeLL[-1])

        if self.position == 1:
            if lPrices[curBarLookBack] <= self.parOp:
                self.position = -1
                self.transition = -1
                self.parCl = self.tradeHH[-1]
                self.tradeHH.append(hPrices[curBarLookBack])
                self.tradeLL.append(lPrices[curBarLookBack])
                self.af = afStep
                self.parOp = self.parCl + self.af * (self.tradeLL[-1] - self.parCl)
                if self.parOp < hPrices[curBarLookBack]: self.parOp = hPrices[curBarLookBack]
                if self.parOp < hPrices[curBarLookBack-1]: self.parOp = hPrices[curBarLookBack-1]
            else:
                self.parCl = self.parOp
                if self.tradeHH[-1] > self.tradeHH[-2] and self.af < afLimit:  #bar array in tradestation
                    self.af = min(self.af + afStep,afLimit)
                self.parOp = self.parCl + self.af * (self.tradeHH[-1] - self.parCl)
#                print("inside ",self.af," ",self.tradeHH[-1])
                if self.parOp > lPrices[curBarLookBack]: self.parOp = lPrices[curBarLookBack]
                if self.parOp > lPrices[curBarLookBack-1]: self.parOp = lPrices[curBarLookBack-1]
        else:
            if hPrices[curBarLookBack] >= self.parOp:
                self.position = 1
                self.transition = 1
                self.parCl = self.tradeLL[-1]
                self.tradeHH.append(hPrices[curBarLookBack])
                self.tradeLL.append(lPrices[curBarLookBack])
                self.af = afStep
                self.parOp = self.parCl + self.af * (self.tradeHH[-1] - self.parCl)
                if self.parOp > lPrices[curBarLookBack]: self.parOp = lPrices[curBarLookBack]
                if self.parOp >lPrices[curBarLookBack-1]: self.parOp = lPrices[curBarLookBack-1]
            else:
                self.parCl = self.parOp
                if self.tradeLL[-1] < self.tradeLL[-2] and self.af < afLimit:
                    self.af = min(self.af + afStep,afLimit)
                self.parOp = self.parCl + self.af * (self.tradeLL[-1] - self.parCl)
                if self.parOp < hPrices[curBarLookBack]: self.parOp = hPrices[curBarLookBack]
                if self.parOp < hPrices[curBarLookBack-1]: self.parOp = hPrices[curBarLookBack-1]

        return(self.parCl,self.parOp,self.position,self.transition)


class adxClass(object):
    def __init__(self):
        self.plusDM =0
        self.minusDM =0
        self.smooth = 0
        self.dmi = list()
        self.adx = list()
        self.adxR = 0
        self.seed= 0
        self.avgPlusDM = list()
        self.avgMinusDM = list()
        self.oVolty= list()

    def calcADX(self,hPrices,lPrices,cPrices,lookBack,curBar,offset):
        curBarLookBack = curBar - offset
        SF = 1 / lookBack
        Divisor = 0
        sumPlusDM = sumMinusDM = sumTR = 0
        if self.seed == 0:
            self.seed = 1
            self.plusDM = self.minusDM = 0
            for cnt in range((curBar - offset) - (lookBack-1),curBar - offset +1):
                upperMove = hPrices[cnt] - hPrices[cnt-1]
                lowerMove = lPrices[cnt-1 ] - lPrices[cnt]
                if upperMove > lowerMove and upperMove > 0:
                    self.plusDM = upperMove
                else:
                    if lowerMove > upperMove and lowerMove > 0:
                        self.minusDM = lowerMove
                sumPlusDM += self.plusDM
                sumMinusDM += self.minusDM
                trueHi = max(cPrices[cnt-1],hPrices[cnt])
                trueLo = min(cPrices[cnt-1],lPrices[cnt])
                sumTR += trueHi - trueLo
            self.avgPlusDM.append(sumPlusDM/ lookBack)
            self.avgMinusDM.append(sumMinusDM/ lookBack)
            self.oVolty.append(sumTR / lookBack )
        else:
       	    self.plusDM = 0
            self.minusDM = 0
            upperMove = hPrices[curBar-offset] - hPrices[curBar-offset-1]
            lowerMove = lPrices[curBar-offset-1] -lPrices[curBar - offset]
            if upperMove > lowerMove and upperMove > 0:
                self.plusDM = upperMove
            else:
                if lowerMove > upperMove and lowerMove > 0:
                    self.minusDM = lowerMove
            self.avgPlusDM.append(self.avgPlusDM[-1] + SF * (self.plusDM - self.avgPlusDM[-1]))
            self.avgMinusDM.append(self.avgMinusDM[-1] + SF * ( self.minusDM - self.avgMinusDM[-1])) ;
            trueHi = max(cPrices[curBar-offset-1],hPrices[curBar - offset])
            trueLo = min(cPrices[curBar-offset-1],lPrices[curBar - offset])
            self.oVolty.append(self.oVolty[-1] + SF * (trueHi - trueLo)- self.oVolty[-1] )

        if self.oVolty[-1] > 0:
        	self.plusDM = 100 * self.avgPlusDM[-1] / self.oVolty[-1]
        	self.minusDM = 100 * self.avgMinusDM[-1] / self.oVolty[-1]
        else:
        	self.plusDM = 0
        	self.minusDM = 0

        Divisor = self.plusDM + self.minusDM
        if Divisor > 0:
        	self.dmi.append(100 * abs( self.plusDM - self.minusDM ) / Divisor)
        else:
        	self.dmi.append(0)

        if len(self.adx) <= lookBack:
            if len(self.dmi) > 1:
                self.adx.append((self.dmi[-1] + self.dmi[-2]) / len(self.adx))
                self.adxR = (self.adx[-1] + self.adx[-(len(self.adx))]) * .5
            else:
                self.adx.append(self.dmi[-1])
                self.adxR = self.adx[-1]
        else:
            self.adx.append(self.adx[-1] + SF * ( self.dmi[-1] - self.adx[-1] ))
            self.adxR = (self.adx[-1] + self.adx[-lookBack])*.5

        return(self.adx[-1],self.adxR,self.dmi[-1])


class stochClass(object):
    def __init__(self):
        self.fastK = 0
        self.fastD = 0
        self.slowD = 0
        self.seed = 0
    def calcStochastic(self,kLen,dLen,dSloLen,hPrices,lPrices,cPrices,curBar,offset):
        curBarLookBack = curBar - offset
        testSeed = self.seed
        if self.seed == 0:
            self.seed = 1
            stoKList =[]
            stoDList = []
            index1 = kLen + dLen
            index2 = dLen -1 + dSloLen - 1
            loopCnt = 0
            for i in range(0,dLen + dSloLen-1):
                loopCnt = loopCnt + 1
                hh = 0
                ll = 9999999
                lowRngBound = curBarLookBack - (index1 - (i))
                highRngBound =curBarLookBack - (index2 - (i))
                for k in range(lowRngBound,highRngBound+1):
                    if hPrices[k] > hh:
                        hh = hPrices[k]
                    if lPrices[k] < ll:
                        ll = lPrices[k]
                if hh - ll == 0.0:
                    hh = ll + 1
                whichClose = curBarLookBack - (index2 -(i))
                tempClose= cPrices[whichClose]
                stoKList.append((cPrices[whichClose] - ll) / (hh - ll) *100)
                lenOfStoKList = len(stoKList)
                self.fastK = stoKList[len(stoKList)-1]
                if (i >= dLen-1):
                    tempSum = 0
                    lowRngBound = len(stoKList)-dLen
                    highRngBound = lowRngBound + dLen
                    for j in range(lowRngBound,highRngBound):
                        tempSum += stoKList[j]
                    stoDList.append(tempSum/dLen)
                    self.fastD = stoDList[len(stoDList)-1]
                if (i == index2):
                    tempSum = 0
                    lowRngBound = len(stoDList) - dSloLen
                    highRngBound = lowRngBound + dSloLen
                    for j in range(lowRngBound,highRngBound):
                        tempSum += stoDList[j]
                    self.slowD = tempSum / dSloLen
        else:
            hh = 0
            ll = 999999
            lowRngBound = curBarLookBack - (kLen - 1)
            highRngBound = curBarLookBack
            for i in range(lowRngBound, highRngBound+1):
                if hPrices[i] > hh:
                    hh = hPrices[i]
                if lPrices[i] < ll:
                    ll = lPrices[i]
            self.fastK = (cPrices[curBarLookBack] - ll )/ (hh - ll) * 100
            self.fastD = ((self.fastD * (dLen - 1)) + self.fastK) / dLen
            self.slowD = ((self.slowD * (dSloLen - 1)) + self.fastD) / dSloLen

        return(self.fastK,self.fastD,self.slowD)


class rsiClass(object):
    oldDelta1 = 0
    def __init__(self):
        self.delta1 = 0
        self.delta2 = 0
        self.rsi = 0
        self.seed = 0
    def calcRsi(self,prices,lookBack,curBar,offset):
        upSum = 0.0
        dnSum = 0.0
        if self.seed == 0:
            self.seed = 1
            for i in range((curBar - offset) - (lookBack-1),curBar - offset +1):
                if prices[i] > prices[i-1]:
                    diff1 = prices[i] - prices[i-1]
                    upSum += diff1
                if prices[i] < prices[i-1]:
                    diff2 = prices[i-1] - prices[i]
                    dnSum += diff2
                self.delta1 = upSum/lookBack
                self.delta2 = dnSum/lookBack
        else:
            if prices[curBar - offset] > prices[curBar - 1 - offset]:
                diff1 = prices[curBar - offset] - prices[curBar - 1 - offset]
                upSum += diff1
            if prices[curBar - offset] < prices[curBar - 1 - offset]:
                diff2 = prices[curBar - 1 - offset] - prices[curBar - offset]
                dnSum += diff2
            self.delta1 = (self.delta1 * (lookBack -1) + upSum) / lookBack
            self.delta2 = (self.delta2 * (lookBack -1) + dnSum) / lookBack
        if self.delta1 + self.delta2 != 0:
            self.rsi = (100.0 * self.delta1) / (self.delta1 + self.delta2)
        else:
            self.rsi = 0.0
        return (self.rsi)

class macdClass(object):
    def __init__(self):
        self.xavg1 = 0
        self.xavg2 = 0
        self.MACD = 0
        self.smoothMACD = 0
        self.rsi = 0
        self.seed = 0
    def calcMacd(self,prices,shortLen, longLen, smooth ,curBar,offset):
        if self.seed == 0:
            self.xavg1 = prices[curBar-offset]
            self.xavg2 = prices[curBar-offset]
            self.MACD = 0
            self.seed = 1
        else:
            self.xavg1 = self.xavg1 + 2 / shortLen * (prices[curBar-offset] - self.xavg1)
            self.xavg2 = self.xavg2 + 2 / longLen * (prices[curBar-offset] - self.xavg2)
            self.MACD  = self.xavg1 - self.xavg2
            self.smoothMACD = self.smoothMACD + 2 / smooth * (self.MACD - self.smoothMACD)
        return(self.MACD, self.smoothMACD)

class dominantCycleClass(object):
    def __init__(self):
        self.imult = 0.635
        self.qmult = 0.338
        self.value1 = [0 for i in range(5)]
        self.inPhase = [0 for i in range(5)]
        self.quadrature = [0 for i in range(5)]
        self.re = [0 for i in range(5)]
        self.im = [0 for i in range(5)]
        self.deltaPhase = [0 for i in range(5)]
        self.instPeriod = [0 for i in range(5)]
        self.period = [0 for i in range(5)]

    def calcDomCycle(self,dates,hPrices,lPrices,cPrices,curBar,offset):
        tempVal1 = (hPrices[curBar - offset] + lPrices[curBar-offset])/2
        tempVal2 = (hPrices[curBar - offset - 7] + lPrices[curBar-offset - 7])/2
        self.value1.append(tempVal1 - tempVal2)
        self.inPhase.append(1.25*(self.value1[-5] - self.imult*self.value1[-3]) + self.imult*self.inPhase[-3])
        self.quadrature.append(self.value1[-3] - self.qmult*self.value1[-1] + self.qmult*self.quadrature[-2])
        self.re.append(.2*(self.inPhase[-1]*self.inPhase[-2]+self.quadrature[-1]*self.quadrature[-2])+ 0.8*self.re[-1])
        self.im.append(.2*(self.inPhase[-1]*self.quadrature[-2] - self.inPhase[-2]*self.quadrature[-1]) +.8*self.im[-1])
        if self.re[-1] != 0.0: self.deltaPhase.append(degrees(atan(self.im[-1]/self.re[-1])))
        if len(self.deltaPhase) > 51:
            self.instPeriod.append(0)
            value4 = 0
            for count in range(1,51):
                value4 += self.deltaPhase[-count]
                if value4 > 360 and self.instPeriod[-1] == 0:
                    self.instPeriod.append(count)
            if self.instPeriod[-1] == 0: self.instPeriod.append(self.instPeriod[-1])
            self.period.append(.25*self.instPeriod[-1]+.75*self.period[-1])
            return(self.period[-1])
        return(50)


def highest(prices,lookBack,curBar,offset):
    result = 0.0
    maxVal = 0.00
    for index in range((curBar - offset) - (lookBack-1),curBar - offset +1):
        if prices[index] > maxVal:
            maxVal = prices[index]
    result = maxVal
    return result

def highest2(prices,lookBack,offset):
    result = 0.0
    maxVal = 0.00
    curBar = len(prices)
    if curBar > lookBack + 1:
        for index in range((curBar - offset) - (lookBack-1),curBar - offset +1):
            if prices[index] > maxVal:
                maxVal = prices[index]
        result = maxVal
    return result


def lowest(prices,lookBack,curBar,offset):
    result = 0.0
    minVal = 9999999.0
    for index in range((curBar - offset) - (lookBack-1),curBar - offset +1):
        if prices[index] < minVal:
            minVal = prices[index]
    result = minVal
    return result

def lowest2(prices,lookBack,offset):
    result = 0.0
    minVal = 9999999.0
    curBar = len(prices)
    if curBar > lookBack + 1:
        for index in range((curBar - offset) - (lookBack-1),curBar - offset +1):
            if prices[index] < minVal:
                minVal = prices[index]
        result = minVal
    return result

def sAverage(prices,lookBack,curBar,offset):
    result = 0.0
    for index in range((curBar - offset) - (lookBack-1),curBar - offset +1):
        result = result + prices[index]
    result = result/float(lookBack)
    return result

def sAverage2(prices,lookBack,offset):
    result = 0.0
    curBar = len(prices)
    if curBar > lookBack + 1:
        for index in range((curBar - offset) - (lookBack-1),curBar - offset +1):
            result = result + prices[index]
        result = result/float(lookBack)
    return result


def xAverage(prices,prevXavg,lookBack,curBar,offset):
    if prevXavg == 0:
        return prices[curBar - offset]
    return prevXavg + 2 / lookBack * (prices[curBar - offset] - prevXavg)

def bollingerBands(dates,prices,lookBack,numDevs,curBar,offset):

    sum1 = 0.0
    sum2 = 0.0
    startPt = (curBar - offset)- (lookBack-1)
    endPt = curBar - offset + 1
#    print(dates[startPt])
    for index in range(startPt,endPt):
        tempDate = dates[index]
        sum1 = sum1 + prices[index]
        sum2 = sum2 + prices[index]**2

    mean = sum1 / float(lookBack)

    stdDev = 0.0
    if lookBack * sum2 > sum1**2 :
        stdDev = ((lookBack * sum2 - sum1**2) / (lookBack * (lookBack -1)))**0.5
    upBand = mean + numDevs*stdDev
    dnBand = mean - numDevs*stdDev


    return upBand, dnBand, mean

def keltnerChannels(dates,multiPrices,lookBack,numAtrs,curBar,offset):
# unpack O,H,L,C and TR from multiPrces
# [0] - open
# [1] - high
# [2] - low
# [3] - close
# [4] - true ranges

    sum1 = 0.0
    sum2 = 0.0
    startPt = (curBar - offset)- (lookBack-1)
    endPt = curBar - offset + 1
    for index in range(startPt,endPt):
        tempDate = dates[index]
        tempHigh = multiPrices[1][index]
        tempLow = multiPrices[2][index]
        tempClose = multiPrices[3][index]
        tempTR = multiPrices[4][index]
        sum1 = sum1 + (tempHigh + tempLow + tempClose)/3.0
        sum2 = sum2 + tempTR

    avgTP = sum1 / float(lookBack)
    atr = sum2 / float(lookBack)

    keltUpChan = avgTP + numAtrs * atr
    keltDnChan = avgTP - numAtrs * atr
    keltAvg = avgTP
    return keltUpChan, keltDnChan, keltAvg

def linearRegression(dates,prices,lookBack,numDaysPredict,curBar,offset):

    mean = sAverage(prices,lookBack, curBar, offset)
    zx = 0
    zy = 0
    zx = 0
    zxy = 0
    zxx = 0
    zyy = 0
    sum1 = 0
    c = 0
    startPt = (curBar - offset)- (lookBack-1)
    endPt = curBar - offset + 1

    for index in range(startPt,endPt):
        c = c + 1
        zx = zx + c
        zy = zy + prices[index]
        zxx = zxx + c ** 2
        zyy = zyy + prices[index] ** 2
        zxy = zxy + c * prices[index]
 #       sum1 = (prices[index] - mean) ** 2


    slope = (c * zxy - zx * zy) / (c * zxx - zx ** 2)
    intercept = (zxx * zy - zx * zxy) / (c * zxx - zx ** 2)
    rsq = (c * zxy - zx * zy) / (((c * zxx - (zx ^ 2)) * (c * zyy - (zy ** 2))) ** 0.5)

    for index in range(c,c+numDaysPredict):
        predictValue = slope * c + intercept
    return predictValue,slope

def choppyMarketFunc(hPrices,lPrices,cPrices,lookBack,curBar,offset):
    if(lookBack!=0):
        hh = highest(hPrices,lookBack,curBar,offset)
        ll = lowest(lPrices,lookBack,curBar,offset)
        denom = hh - ll
        num =cPrices[(curBar - offset)- (lookBack-1)]- cPrices[curBar - offset]
        num = abs(num)
        if (denom != 0):
            return(num/denom * 100)



