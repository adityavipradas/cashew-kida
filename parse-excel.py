# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 23:47:06 2013

@author: adityavipradas
"""

import xlrd
import matplotlib.pyplot as plt
book = xlrd.open_workbook("cashew-data51.xls")
sheet = book.sheet_by_index(0)
col = 2 #breadth column (constant)
breadth = [] #initiate list
small =[]
large =[]
med =[]

for row in range(1, sheet.nrows):
    val = sheet.cell_value(row, col)
    breadth.append(int(val))
    if (val > 22):
        large.append(val)
    elif (val < 20):
        small.append(val)
    else:
        med.append(val)
print "breadth values\n"
print "mean breadth =",(sum(large) + sum(small) + sum(med))/len(breadth),"mm\n"
print "large:", len(large),"\n\n",large,"\n\nsmall:", len(small), "\n\n", small,"\n\nmedium:", len(med), "\n\n", med
plt.hist(breadth)
plt.title("frequency-breadth histogram")
plt.xlabel("cashewnut breadth(mm)")
plt.ylabel("frequency")
plt.show()
