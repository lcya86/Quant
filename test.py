#-*- coding:UTF-8 -*-
from WindPy import *
import time
w.start()
#print time.strftime("%Y-%m-%d",time.localtime(int(time.time())))
stocks = [u'600028.SH',u'600048.SH',u'600035.SH']
history = w.wsd(stocks, "high", "ED-56TD", time.strftime("%Y-%m-%d",time.localtime(int(time.time()))), "")
print history.Data
d = w.tdayscount('2015-05-1','2015-05-1')
print d.Data[0][0]
