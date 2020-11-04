#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      George
#
# A class that determines if the last trade was a loser based on
# user input
#
# Created:     03/08/2020
# Copyright:   (c) George 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from math import log10
class ltlClass(object):
    def __init__(self):
        self.state = 0
        self.theoMP = 0
        self.theoEP = 0
        self.theoEX = 0
        self.ltl = 1
        self.ltlBenchMark= 0
#def lastTradeLoser(curState,myOp,myHi,myLo,curBar,lep,sep,lxpIsLoser,sxpIsLoser,anchor,lxpAlt,sxpAlt,ltlBenchMark,theoMP):
##    def setLTLValues(self,state,theoMP,theoEP,theoEX,ltlBenchMark):
##        self.state = state
##        self.theoMP = theoMP
##        self.theoEP = theoEP
##        self.theoEX = theoEx
##        self.ltlBenchMark = ltlBenchMark

    def lastTradeLoser(self,myOp,myHi,myLo,curBar,lep,sep,isValueAPrice,lxpIsLoser,sxpIsLoser,anchor,lxpAlt,sxpAlt,anyLossIsLoser):
        seekLong = True
        seekShort = True
#        isValueAPrice = True
        cantExitToday = False
#        if abs(log10(abs(myOp[curBar])) - log10(abs(lxpIsLoser)))>=1.0: isValueAPrice = False
        for i in range(0,2):
            if self.state==0:
                if seekLong and myHi[curBar]>= lep:
                    self.theoMP = 1
                    self.theoEP= max(myOp[curBar],lep)
                    if isValueAPrice:
                        self.theoEX = lxpIsLoser
                    else:
                        self.theoEX = self.theoEP-lxpIsLoser
#                    print(" Going Long at ",self.theoEP," ",self.theoEX)
                if seekShort and myLo[curBar]<= sep:
                    self.theoMP = -1
                    self.theoEP= min(myOp[curBar],sep)
                    if isValueAPrice:
                        self.theoEX = sxpIsLoser
                    else:
                        self.theoEX = self.theoEP+sxpIsLoser
#                    print(" Going Short at ",self.theoEP," ",self.theoEX," ",isValueAPrice," ",sxpIsLoser)
                if self.theoMP !=0:
                    self.state = 1
                    cantExitToday = True
            if self.state == 1:
                if not(cantExitToday):
                    if not(anchor):
                        if self.theoMP == 1:
                            if isValueAPrice: self.theoEX = lxpIsLoser
                            else: self.theoEX = self.theoEP - lxpIsLoser
                        if self.theoMP ==-1:
                            if isValueAPrice: self.theoEX = sxpIsLoser
                            else: self.theoEX = self.theoEP + sxpIsLoser
                    whichLxp = max(self.theoEX,lxpAlt)
                    whichSxp = min(self.theoEX,sxpAlt)

                    if self.theoMP == 1:
                        if sep < self.theoEX:
                            self.ltlBenchMark = sep
                        else:
                            self.ltlBenchMark = 0

                    if self.theoMP == -1:
                        if lep > self.theoEX:
                            self.ltlBenchMark = lep
                        else:
                            self.ltlBenchMark = 999999999

                    if self.theoMP == 1 and myLo[curBar]<=whichLxp:
                        self.theoMP = 0
                        seekLong = False
#                        print(" LongExit at ",whichLxp," ",whichLxp <=self.theoEP)
                        cond1 = whichLxp <= self.theoEX
                        cond2 = whichLxp < self.theoEP
                        if anyLossIsLoser:
                            cond1 = True
                        if cond1 and cond2:
                            self.ltl = True
                        else:
                            self.ltl = False
                    if self.theoMP ==-1 and myHi[curBar]>=whichSxp:
                        self.theoMP = 0
                        seekShort = False
#                        print("ShortExit at ",whichSxp," ",whichSxp >=self.theoEP)
                        cond1 = whichSxp >= self.theoEX
                        cond2 = whichSxp > self.theoEP
                        if anyLossIsLoser:
                            cond1 = True
                        if cond1 and cond2:
                            self.ltl = True
                        else:
                            self.ltl = False
                    if self.theoMP == 0: self.state = 0
        cantExitToday = False
        return(self.ltl)
