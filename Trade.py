# -*- coding: utf-8 -*-
#如果当前价格高于最高价格，则更新最高价格；
#如果最高价格与当前价格的差价大于等于成本价格的7%，则止损；
def TrackPrice(indata):
    global MAX_PRICE
    global w
    global StockCode
    global pf
    global COST_PRICE
    global STOP_RATE
    global LOGONID
    global IS_HOLD

    print indata
          
    if indata.ErrorCode!=0:
        print('error code:'+str(indata.ErrorCode)+'\n')
        return();

    buyprice = 0;
    sellprice = 0;
    for k in range(0,len(indata.Fields)):
        if(indata.Fields[k] == "rt_bid1"):
            buyprice = str(indata.Data[k][0])
        if(indata.Fields[k] == "rt_ask1"):
            sellprice = str(indata.Data[k][0])
            MAX_PRICE = sellprice

    if (not IS_HOLD)and(sellprice>=MAX_PRICE):
        w.torder(StockCode,"Buy",sellprice,POSITION,logonid=LOGONID)
        COST_PRICE = sellprice+(POSITION*sellprice*0.00025)
        IS_HOLD = True

    if (buyprice > MAX_PRICE):
        MAX_PRICE = buyprice
        string = u"买1:" + str(buyprice) +"\n"
        pf.writelines(string)
    elif IS_HOLD and (MAX_PRICE - buyprice)>=COST_PRICE*STOP_RATE:
        w.torder(StockCode,"Sell",buyprice,POSITION,logonid=LOGONID)

    result = str(indata.Times[0])+" IS_HOLD:"+str(IS_HOLD)+" COST_PRICE:"+str(COST_PRICE)+" MAX_PRICE:"+str(MAX_PRICE)+"\n"
    pf.writelines(result)
    print result
    return()
    #应该在w.cancelRequest后调用pf.close()
    #pf.close();
