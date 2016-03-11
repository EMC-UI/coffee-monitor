#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy
from numpy import *
import csv
import matplotlib.pyplot as plot
import scipy.signal as signal
import scipy.stats as stats

filterOrder = 2
cutoffFreq = 0.03

sampleWindow = 60
#startIndex = 790
startIndex = 780
stopIndex = startIndex + sampleWindow

with open('lower-once.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

indexes = [int(x[0]) for x in your_list[1:-1]]
xvalues = [float(x[1]) for x in your_list[1:-1]]

onlyDownslopeIndexes = indexes[startIndex: stopIndex]
onlyDownslopeValues = xvalues[startIndex: stopIndex]

# lets try a lowpass filter
B, A = signal.butter(filterOrder, cutoffFreq)
xvaluesNPArray = numpy.array(onlyDownslopeValues)
xvaluesFiltered = signal.filtfilt(B, A, xvaluesNPArray)
allXFiltered = signal.filtfilt(B,A, numpy.array(xvalues))

x1 = signal.filtfilt(B,A, numpy.array(xvalues[100:400]))
x2 = signal.filtfilt(B,A, numpy.array(xvalues[200:500]))
corr1 = stats.pearsonr(x1,x2)
corr2 = stats.spearmanr(x1,x2)
print('1 correlation between x1 and x2 is {0:2.3f} , {1:2.3f}'.format(corr1[0], corr1[1]))
print('2 correlation between x1 and x2 is {0:2.3f} , {1:2.3f}'.format(corr2[0], corr2[1]))

#plot.plot(onlyDownslopeIndexes, onlyDownslopeValues)
#plot.plot(onlyDownslopeIndexes, xvaluesFiltered)

polyCoeff = numpy.polyfit(onlyDownslopeIndexes, xvaluesFiltered, 4)
print('slope {0:2.10f}'.format(polyCoeff[0]))
print('slope {0:2.10f}'.format(polyCoeff[1]))
print('slope {0:2.10f}'.format(polyCoeff[2]))
print('slope {0:2.10f}'.format(polyCoeff[3]))
print('slope {0:2.10f}'.format(polyCoeff[4]))
polyFunc = numpy.poly1d(polyCoeff)


ys = polyFunc(onlyDownslopeIndexes)

#plot.plot(onlyDownslopeIndexes, ys)
plot.plot(indexes, allXFiltered)
plot.show()
