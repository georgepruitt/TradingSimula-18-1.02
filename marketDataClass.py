
class marketDataClass(object):
    def __init__(self):
        self.symbol = ""
        self.minMove = 0
        self.bigPtVal = 0
        self.longName =""
        self.seed = 0
        self.date = list()
        self.open = list()
        self.high = list()
        self.low = list()
        self.close = list()
        self.volume = list()
        self.opInt = list()
        self.range = list()
        self.trueRange = list()
        self.dataPoints = 0
    def setDataAttributes(self,symbol,longName,bigPtVal,minMove):
        self.symbol = symbol
        self.minMove = minMove
        self.bigPtVal = bigPtVal
        self.longName = longName
    def readData(self,date,open,high,low,close,volume,opInt):
        self.date.append(date)
        self.open.append(open)
        self.high.append(high)
        self.low.append(low)

        if len(self.date) > 1:
            self.trueRange.append(max(self.close[-1],high) - min(self.close[-1],low))
        else:
            self.trueRange.append(high - close)
        self.close.append(close)
        self.volume.append(volume)
        self.opInt.append(opInt)
        self.range.append(high - low)
        self.dataPoints += 1

