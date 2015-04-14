#-*- coding:UTF-8 -*-
from datetime import *
import threading

def isBegin():
    if datetime.now().time()>time(9,29,59) and datetime.now().time()<time(11,30,0):
        return True
    elif datetime.now().time()>time(12,59,59) and datetime.now().time()<time(15,0,0):
        return True
    else:
        return False
