
def assignSectors(symbolList):
    sector1 = list()
    sector2 = list()
    sector3 = list()
    sector4 = list()
    sector5 = list()
    sector6 = list()
    sector7 = list()
    sector8 = list()

    if "BP" in symbolList: sector1.append("BP")
    if "SF" in symbolList: sector1.append("SF")
    if "AD" in symbolList: sector1.append("AD")
    if "DX" in symbolList: sector1.append("DX")
    if "EC" in symbolList: sector1.append("EC")
    if "JY" in symbolList: sector1.append("JY")
    if "CD" in symbolList: sector1.append("CD")

    if "CL" in symbolList: sector2.append("CL")
    if "HO" in symbolList: sector2.append("HO")
    if "NG" in symbolList: sector2.append("NG")
    if "RB" in symbolList: sector2.append("RB")

    if "GC" in symbolList: sector3.append("GC")
    if "SI" in symbolList: sector3.append("SI")
    if "HG" in symbolList: sector3.append("HG")
    if "PL" in symbolList: sector3.append("PL")
    if "PA" in symbolList: sector3.append("PA") 
    
    if "S_" in symbolList: sector4.append("S_")
    if "W_" in symbolList: sector4.append("W_")
    if "C_" in symbolList: sector4.append("C_")
    if "BO" in symbolList: sector4.append("BO")
    if "SM" in symbolList: sector4.append("SM")
    if "RR" in symbolList: sector4.append("RR")
    if "KW" in symbolList: sector4.append("KW")

    if "US" in symbolList: sector5.append("US")
    if "TY" in symbolList: sector5.append("TY")
    if "TU" in symbolList: sector5.append("TU")
    if "FV" in symbolList: sector5.append("FV")
    if "ED" in symbolList: sector5.append("ED")  

    if "SB" in symbolList: sector6.append("SB")
    if "KC" in symbolList: sector6.append("KC")
    if "CC" in symbolList: sector6.append("CC")
    if "CT" in symbolList: sector6.append("CT")
    if "LB" in symbolList: sector6.append("LB")
    if "OJ" in symbolList: sector6.append("OJ")
    
    if "LC" in symbolList: sector7.append("LC")
    if "LH" in symbolList: sector7.append("LH")
    if "FC" in symbolList: sector7.append("FC")

    return(sector1,sector2,sector3,sector4,sector5,sector6,sector7,sector8)


        
