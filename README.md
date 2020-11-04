# TradingSimula-18-1.02
Version using Open PyXL and Long Com Names
In some cases like Pinnacle Data the symbol Names don't make sense - so I added an additional field in the DataMaster that contains the long commodity name.
Here is an example - 
"PINDATA",0,0.0,"A"
"AN",1000,0.01,"Aus.Dol"
"ZL",600,0.01,"BeanOil"
"BN",625,0.01,"B.Pound"
"ZU",1000,0.01,"Crude"
"ZC",50,0.25,"Corn"
"CC",10,1,"Cocoa"
"CN",1000,0.01,"Can.Dol"
"CT",500,0.01,"Cotton"
"FN",1250,0.005,"EuroCur"
"DX",1000,0.005,"DolIndx"
"ED",2500,0.0025,"EuroDol"
"EM",100,0.1,"MidCap"
"MD",100,0.1,"MidCap"

So reading this data required modifications in several modules inlcuding all of the main strategy modules.
