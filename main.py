#-*- coding:UTF-8 -*-
from WindPy import *
import Select
import Timer
from datetime import *
from time import sleep



MAX_PRICE = 7.28
COST_PRICE = 7.0877
STOP_RATE = 0.05
POSITION = 500000
IS_HOLD = True
LOGONID = 0
IS_STOP = True
StockCode = ''



#如果当前价格高于最高价格，则更新最高价格；
#如果最高价格与当前价格的差价大于等于成本价格的7%，则止损；
def TrackPrice(indata,POSITION,STOP_RATE,LOGONID):
    global MAX_PRICE
    global COST_PRICE
    global IS_HOLD
          
    if indata.ErrorCode!=0:
        print('error code:'+str(indata.ErrorCode)+'\n')
        return();

    buyprice = 0;
    sellprice = 0;
    for k in range(0,len(indata.Fields)):
        if(indata.Fields[k] == "RT_BID1"):
            buyprice = indata.Data[k][0]
        if(indata.Fields[k] == "RT_ASK1"):
            sellprice = indata.Data[k][0]

    if (not IS_HOLD)and(sellprice>=MAX_PRICE):
        w.torder(StockCode,"Buy",sellprice,POSITION,logonid=LOGONID)
        COST_PRICE = sellprice
        IS_HOLD = True
        result = str(indata.Times[0])+' buy@'+str(sellprice)
        pf.writelines(result)
        print result

    if (buyprice > MAX_PRICE):
        MAX_PRICE = buyprice
        result = 'MAX_PRICE:'+str(MAX_PRICE)
        pf.writelines(result)
        print result
    elif IS_HOLD and (MAX_PRICE - buyprice)>=COST_PRICE*STOP_RATE:
        w.torder(StockCode,"Sell",buyprice,POSITION,logonid=LOGONID)
        IS_HOLD = False
        profit = (COST_PRICE-buyprice)/COST_PRICE
        result = str(indata.Times[0])+' sell@'+str(buyprice)+' profit:'+str(profit)
        pf.writelines(result)
        print result

    return()
    #应该在w.cancelRequest后调用pf.close()
    #pf.close();

w.start()
while True:
    if Timer.isBegin():
        pf = open('D:\\Github\\Quant\\traderecord.txt', 'w')
        LOGONID = w.tlogon("00000010","0","M:1521058274301","******","SHSZ").Data[0]
        Position = w.tquery("Position",logonid=LOGONID)
        StockCode = Select.BollSelection()
        print "StockCode:"+StockCode

    while Timer.isBegin():
        data = w.wsq(StockCode,"rt_bid1,rt_ask1")
        TrackPrice(data,POSITION,STOP_RATE,LOGONID)
        Position = w.tquery("Position",logonid=LOGONID)
        sleep(1)








        
        
