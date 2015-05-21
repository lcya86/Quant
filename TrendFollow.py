#-*- coding:UTF-8 -*-
from WindPy import *
import Timer
import time

class Context(object):
    logonid = 0
    #中信证券、唐山港、楚天高速、北方导航、中国北车、南方航空、长安汽车、平安银行、科大讯飞、保利地产、中联重科、淮柴动力、泸州老窖、四环生物、泰山石油、国电电力、凤凰股份、华仪电气、中国西电、天津海运
    #stocks = [u'600030.SH',u'601000.SH',u'600035.SH',u'600435.SH',u'601299.SH',u'600029.SH',u'000625.SZ',u'000001.SZ',u'002230.SZ',u'600048.SH',u'000157.SZ',u'000338.SZ',u'000568.SZ',u'000518.SZ',u'000554.SZ',u'600795.SH',u'600716.SH',u'600290.SH',u'601179.SH',u'600751.SH']
    stocks = [u'600028.SH',u'600048.SH',u'600035.SH']
    traded = [False]*len(stocks)
    maxprice = [0]*len(stocks)
    cash = [0]*len(stocks)
    stoprate = 0.04

    def __init__(self):
        self.logonid = w.tlogon("00000010","0","M:1521058274301","123456","SHSZ").Data[0]
        self.fp = open('trade.data','r+')
        templist = self.fp.readlines()
        self.fp.close()

        if templist != [] and templist[0] != '':
            self.cash = [float(i) for i in templist[0].replace('[','').replace(']','').replace(' ','').split(',')]
        else:
            Capital = w.tquery("Capital",logonid=self.logonid)
            if Capital.ErrorCode!=0:
                print('Capital error code:'+str(Capital.ErrorCode)+'\n')
            else:
                self.cash = [Capital.Data[1][0]/len(self.stocks)]*len(self.stocks)

        self.getHistory()
        

        

    def logon(self):
        if not w.isconnected():
            self.logonid = w.tlogon("00000010","0","M:1521058274301","123456","SHSZ").Data[0]
            print "LOGONID:"+str(self.logonid)

    def getPosition(self):
        self.Position = w.tquery("Position",logonid=self.logonid)
        

    def getPrice(self):
        self.Price = w.wsq(self.stocks,"rt_bid1,rt_ask1")

    def getHistory(self):
        today = time.strftime("%Y-%m-%d",time.localtime(int(time.time())))
        history = w.wsd(self.stocks, "high", "ED-60D",today, "Fill=Previous;Currency=CNY")
        if history.ErrorCode!=0:
            print('history error code:'+str(history.ErrorCode)+'\n')
            return self.getHistory()
        else:
            print('history get!\n')
            for index,stock in enumerate(self.stocks):
                self.maxprice[index] = history.Data[index][0]



def Trade(context,index):
    stockcode = context.stocks[index]
    if len(context.Position.Data)>3:
        if stockcode in context.Position.Data[0]:
            query_index = context.Position.Data[0].index(stockcode)
        else:
            query_index = -1
            
    if context.Price.ErrorCode!=0:
        print('Price error code:'+str(context.Price.ErrorCode)+'\n')
        if context.Price.ErrorCode==-40520008:
            context.logon()
        return()

    if context.Position.ErrorCode!=0:
        print('Position error code:'+str(context.Position.ErrorCode)+'\n')
        if context.Position.ErrorCode==-40520008:
            context.logon()
        return()

    buy_1 = 0;
    sell_1 = 0;
    for k in range(0,len(context.Price.Fields)):
        if(context.Price.Fields[k] == "RT_BID1"):
            buy_1 = context.Price.Data[k][index]
            if buy_1 == 0:
                return()
        if(context.Price.Fields[k] == "RT_ASK1"):
            sell_1 = context.Price.Data[k][index]
            if sell_1 == 0:
                return()

    
    if len(context.Position.Data)<=3 or query_index == -1:
        hold_volume = 0
        cost_price = 0
    else:
        hold_volume = context.Position.Data[3][query_index]
        cost_price = context.Position.Data[9][query_index]

    if context.maxprice[index] == 0:
        context.maxprice[index] = sell_1;
       
    if buy_1 > context.maxprice[index] and context.cash[index] > sell_1*100 and traded[index] == False:
        buy_volume = int(context.cash[index]/(sell_1*100))*100
        result = w.torder(context.stocks[index],"Buy",sell_1,buy_volume,logonid=context.logonid)
        context.cash[index] = context.cash[index] - (sell_1*buy_volume)
        traded[index] = True
        #print result
        print 'buy '+context.stocks[index]+' '+str(buy_volume)+'@'+str(sell_1)+'\n'
    elif sell_1 < (context.maxprice[index] - context.stoprate*cost_price) and hold_volume > 0 and traded == False:
        result = w.torder(context.stocks[index],"Sell",buy_1,hold_volume,logonid=context.logonid)
        context.maxprice[index] = buy_1
        context.cash[index] = context.cash[index] + (buy_1*hold_volume)
        traded[index] = True
        #print result
        print 'sell '+context.stocks[index]+' '+str(hold_volume)+'@'+str(buy_1)+'\n'

    return()
        

w.start()
context = Context()
while True:
    while Timer.almostEnd():
        context.logon()
        context.getPosition()
        context.getPrice()
        for index,stock in enumerate(context.stocks):
            Trade(context,index)

        fp = open('trade.data','w')
        fp.write(str(context.cash))
        fp.close()
        time.sleep(10)








        
        
