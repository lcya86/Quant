#-*- coding:UTF-8 -*-
from WindPy import *
import Select
import Timer
from datetime import *
from time import sleep

class Context(object):
    logonid = 0
    #中信证券、唐山港、楚天高速、北方导航、中国北车、南方航空、比亚迪、平安银行、科大讯飞、保利地产
    stocks = ['600030.sh','601000.sh','600035.sh','600435.sh','601299.sh','600029.sh','002594.sz','000001.sz','002230.sz','600048.sh']
    maxprice = [0]*len(stocks)
    stoprate = 0.07

    def __init__(self):
        self.logonid = w.tlogon("00000010","0","M:1521058274301","******","SHSZ").Data[0]
        Capital = w.tquery("Capital",logonid=self.logonid)
        if Capital.ErrorCode!=0:
            print('Capital error code:'+str(Capital.ErrorCode)+'\n')
            self.cash = [0]*len(self.stocks)
        else:
            self.cash = Capital.Data[1][0]/len(self.stocks)

    def relogon(self):
        self.logonid = w.tlogon("00000010","0","M:1521058274301","******","SHSZ").Data[0]



def Trade(context,index,Position,Price):
    if Price.ErrorCode!=0:
        print('Price error code:'+str(Price.ErrorCode)+'\n')
        if Price.ErrorCode==-40520008:
            context.relogon()
        return()

    if Position.ErrorCode!=0:
        print('Position error code:'+str(Position.ErrorCode)+'\n')
        if Position.ErrorCode==-40520008:
            context.relogon()
        return()

    buy_1 = 0;
    sell_1 = 0;
    for k in range(0,len(Price.Fields)):
        if(Price.Fields[k] == "RT_BID1"):
            buy_1 = Price.Data[k][index]
        if(Price.Fields[k] == "RT_ASK1"):
            sell_1 = Price.Data[k][index]
    
    current_price = Position.Data[11][index]
    hold_volume = Position.Data[3][index]
    cost_price = Position.Data[9][index]
    if current_price > context.maxprice[index] and context.cash[index] > current_price*100:
        buy_volume = int(context.cash[index]/(current_price*100)/2)*100
        result = w.torder(context.stocks[index],"Buy",sell_1,volume,logonid=context.logonid)
        context.cash[index] = context.cash[index] - (sell_1*volume)
        print result
        print 'buy '+context.stocks[index]+''+str(volume)+'@'+str(sell_1)+'\n'
    elif current_price < (context.maxprice[index] - context.stoprate*cost_price) and hold_volume > 0:
        result = w.torder(context.stocks[index],"Sell",buy_1,hold_volume,logonid=context.logonid)
        context.cash[index] = context.cash[index] + (buy_1*hold_volume)
        print result
        print 'sell '+context.stocks[index]+''+str(hold_volume)+'@'+str(buy_1)+'\n'

    if current_price > context.maxprice[index]:
        context.maxprice[index] = current_price

    return()
        

w.start()
context = Context()
while True:
    if Timer.isBegin():
        #pf = open('D:\\Github\\Quant\\traderecord.txt', 'w')
        context.logonid = w.tlogon("00000010","0","M:1521058274301","******","SHSZ").Data[0]
        print "LOGONID:"+str(context.logonid)

    while Timer.isBegin():
        Position = w.tquery("Position",logonid=context.logonid)
        Price = w.wsq(context.stocks,"rt_bid1,rt_ask1")
        
        
        for index,stock in enumerate(context.stocks):
            Trade(context,index,Position,Price)
            
        sleep(60)








        
        
