#-*- coding:UTF-8 -*-
from WindPy import *
w.start()
history = w.wsd("600000.SH", "high", "ED-60D", "2015-05-18")
print history
