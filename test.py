#-*- coding:UTF-8 -*-
'''
fp = open("a.txt",'w')
o = [12,23.4,122,444]
fp.write(str(o)+'\n')
fp.write(str(o))
fp.close()
'''
fp = open('a.txt','r+')
templist = fp.readlines()
for a in templist:

  c = [float(i) for i in a.replace('[','').replace(']','').replace(' ','').split(',')]
  print c

