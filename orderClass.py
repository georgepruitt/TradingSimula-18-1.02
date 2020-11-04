#-------------------------------------------------------------------------------
# Name:        orderClass
# Purpose:
#
# Author:      George
#
# Created:     26/05/2020
# Copyright:   (c) George 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class orderClass(object):
    def __init__(self):
        self.sysName = ""
        self.comName =""
        self.curMarket = 0
        self.marketPos= 0
        self.orderDate = 0
        self.entryPrice = 0
        self.barsSinceEntry = 0
        self.maxContractProfit = 0
        self.currentProfit = 0
        self.numShares = 0
        self.posSize = 0
        self.myBPV = 0
        self.ohlc = list()
        self.calcVals = list()
        self.params = list()


##def printOutOrders(listOfOrders):
##        for i in range(0,len(listOfOrders)):
##            print(listOfOrders[i].sysName)
##            print(listOfOrders[i].comName)
##            print(listOfOrders[i].orderDate)
##            for j in len(listOfOrders[i].orderDirList):
##                print(listOfOrders[i].orderDirList[j]," ",listOfOrders[i].orderDirList[j])

def generateOrdersFunc(tempOrders,createNewSheet):

    o = tempOrders.ohlc[0][0]
    h = tempOrders.ohlc[0][1]
    l = tempOrders.ohlc[0][2]
    c = tempOrders.ohlc[0][3]
    myBPV = tempOrders.myBPV
    mp = tempOrders.marketPos
    numShares = tempOrders.numShares
    posSize = numShares + tempOrders.posSize
    entryPrice = tempOrders.entryPrice
    barsSinceEntry = tempOrders.barsSinceEntry
    maxContractProfit = tempOrders.maxContractProfit
    currentProfit = tempOrders.currentProfit



    if tempOrders.sysName == 'Andromeda':
        fileName1 = tempOrders.sysName + "-Orders.txt"
        if createNewSheet:
            target1 = open(fileName1,"w")
        else:
            target1 = open(fileName1,"a+")

        orderPlaced =  0
        Value1 = tempOrders.calcVals[0][0]
        Value2 = tempOrders.calcVals[0][1]
        Value3 = tempOrders.calcVals[0][2]
        Value4 = tempOrders.calcVals[0][3]
        Value5 = tempOrders.calcVals[0][4]
        Value6 = tempOrders.calcVals[0][5]
        Value7 = tempOrders.calcVals[0][6]
        Value8 = tempOrders.calcVals[0][7]
        Upper_Band = tempOrders.calcVals[0][8]
        Lower_Band = tempOrders.calcVals[0][9]
        Initial_Risk = tempOrders.params[0]

        lineOutPut = "-------------------------------------------------------\n"
        target1.write(lineOutPut)
        lineOutPut = "Sys Name : " + tempOrders.sysName
        target1.write(lineOutPut)
        target1.write("\n")
        lineOutPut = "Orders for: "+ tempOrders.comName +" - Last Data Date: "+str(tempOrders.orderDate)
        target1.write(lineOutPut)
        target1.write("\n")

        lineOutPut = "Current Position is: " + str(mp)+ " BarsSinceEntry is: "+ str(barsSinceEntry)
        target1.write(lineOutPut)
        target1.write("\n")

        lineOutPut = "Max Contract Profit is: " + str(round(maxContractProfit,0)) + " Current Profit is: " + str(round(currentProfit,0))
        target1.write(lineOutPut)
        target1.write("\n")

        lineOutPut = "-------------------------------------------------------\n"
        target1.write(lineOutPut)

        lineOutPut = ' -----> '
        if c > Value2 and c > Upper_Band and Value7 < Initial_Risk and mp !=1 :
            linOutPut = lineOutPut + "Go Long Next Bar At Open : " + str(posSize) + ' contracts \n'
            orderPlaced+=1
        if mp == 1 and maxContractProfit > Value7 and c < entryPrice and barsSinceEntry > 1:
            linOutPut = lineOutPut + "Liq. Long #1 next bar At Open " + str(numShares) + ' contracts \n'
            orderPlaced+=1
        if mp == 1 and (c - entryPrice)*myBPV > 10000 and barsSinceEntry > 1:
            linOutPut = lineOutPut + "Liq. Long #2 next bar At Open " + str(numShares) + ' contracts \n'
            orderPlaced+=1
        if mp == 1 and barsSinceEntry > 99 and c < Value4 :
            linOutPut = lineOutPut + "Liq. Long #3 next bar At Open " + str(numShares) + ' contracts \n'
            orderPlaced+=1
        if mp == 1 and barsSinceEntry > 74 and c < Value5 :
            linOutPut = lineOutPut + "Liq. Long #4 next bar At Open " + str(numShares) + ' contracts \n'
            orderPlaced+=1
        if mp == 1 and barsSinceEntry > 49 and c < Value6 :
            linOutPut = lineOutPut + "Liq. Long #5 next bar At Open " + str(numShares) + ' contracts \n'
            orderPlaced+=1
        if mp == 1 and barsSinceEntry > 1 and c < Value1 :
            linOutPut = lineOutPut + "Liq. Long #6 next bar At Open " + str(numShares) + ' contracts \n'
            orderPlaced+=1

        if c < Value3 and c < Lower_Band and Value8 < Initial_Risk and mp !=-1 :
            linOutPut = lineOutPut + "Go Short Next Bar At Open : " + str(posSize) + ' contracts \n'
            orderPlaced+=1
        if mp ==-1 and maxContractProfit > Value8 and c > entryPrice and barsSinceEntry > 1:
            linOutPut = lineOutPut + "Liq. Short #1 next bar At Open  " + str(numShares) + ' contracts \n'
            orderPlaced+=1
        if mp == -1 and (entryPrice-c)*myBPV > 10000 and barsSinceEntry > 1:
            linOutPut = lineOutPut + "Liq. Short #2 next bar At Open  " + str(numShares) + ' contracts \n'
            orderPlaced+=1
        if mp == -1 and barsSinceEntry > 99 and c > Value4 :
            linOutPut = lineOutPut + "Liq. Short #3 next bar At Open  " + str(numShares) + ' contracts \n'
            orderPlaced+=1
        if mp == -1 and barsSinceEntry > 74 and c > Value5 :
            linOutPut = lineOutPut + "Liq. Short #4 next bar At Open  " + str(numShares) + ' contracts \n'
            orderPlaced+=1
        if mp == -1 and barsSinceEntry > 49 and c > Value6 :
            linOutPut = lineOutPut + "Liq. Short #5 next bar At Open  " + str(numShares) + ' contracts \n'
            orderPlaced+=1
        if mp == -1 and barsSinceEntry > 1 and c > Value1 :
            linOutPut = lineOutPut + "Liq. Short #6 next bar At Open  " + str(numShares) + ' contracts \n'
            orderPlaced+=1

        if orderPlaced == 0 : lineOutPut = lineOutPut + "No Orders Today -- Current Size: " + str(numShares) + ' contracts \n'
        target1.write(lineOutPut)


    lineOutPut = "-------------------------------------------------------\n"
    target1.write(lineOutPut)
