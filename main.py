#-*- coding:UTF-8 -*-
from WindPy import *
import Select
import Trade
import Timer
from datetime import *
from time import sleep


MAX_PRICE = 0
COST_PRICE = 0
STOP_RATE = 0.05
POSITION = 100000
IS_HOLD = False
LOGONID = 0
IS_STOP = True


w.start()
while True:
    if Timer.isBegin():
        pf = open('C:\\Users\\ben\\Documents\\Quant\\traderecord.txt', 'w')
        LOGONID = w.tlogon("00000010","0","M:1521058274301","******","SHSZ").Data[0]
        Position = w.tquery("Position",logonid=LOGONID)
        StockCode = Select.BollSelection()
        print "StockCode:"+StockCode

    while Timer.isBegin():
        data = w.wsq(StockCode,"rt_bid1,rt_ask1")
        Trade.TrackPrice(data)
        Position = w.tquery("Position",logonid=LOGONID)
        print Position
        sleep(1)








        
        
