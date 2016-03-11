#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy
from numpy import *
import csv
import matplotlib.pyplot as plot
import scipy.signal as signal
import scipy.stats as stats

signatureStart = 800
signatureEnd = 875
B, A = signal.butter(2, 0.03)

with open('lower-once.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

with open('raise-lower-3-times.csv', 'rb') as f:
    reader = csv.reader(f)
    threeTimes = list(reader)

threeValues = [float(x[1]) for x in threeTimes[1:-1]]
threeIndex = range(0, len(threeValues))
threeValuesFiltered = signal.filtfilt(B, A, threeValues)

print('len of threeValuesFiltered {0}'.format(len(threeValuesFiltered)))

otherSignature = threeValuesFiltered[733:818]
flatLine = threeValuesFiltered[2667:2921]

print('len of otherSignature {0}'.format(len(otherSignature)))

indexes = [int(x[0]) for x in your_list[1:-1]]
xvalues = [float(x[1]) for x in your_list[1:-1]]

filteredSignal = signal.filtfilt(B, A, numpy.array(xvalues))

signature = xvalues[signatureStart:signatureEnd]
filteredSignature = signal.filtfilt(B, A, numpy.array(signature))

corr = numpy.correlate(flatLine, filteredSignal, 'same')
conv = numpy.convolve(flatLine, filteredSignal)

# use numpy to do an fft of all the samples
fourier = numpy.fft.fft(filteredSignal)
fftData = numpy.abs(fourier[0:len(fourier) / 2 + 1]) / len(filteredSignal)

frequency = []
freqStrengthPairs = []

# collect the data
for loop in range(len(filteredSignal) / 2 + 1):
    # this builds a list of all the different frequencies
    frequency.append(float(loop) * float(1) / float(len(filteredSignal)))
    # spectrumOutputFile.write("{0:10.2f},{1:10.20f}\n".format(frequency[loop], fftData[loop]))
    d = {'freq': frequency[loop], 'strength': fftData[loop]}
    freqStrengthPairs.append(d)

sigStren = [rec['strength'] for rec in freqStrengthPairs[1:-1]]
freq2 = frequency[1:-1]

# plot.plot(indexes, filteredSignal, 'b-')
# plot.plot(range(0, len(conv)-1), conv[0:-1], 'r-')
# plot.plot(range(0, len(corr)), corr, 'g-')
# plot.plot(range(800, 800 + len(otherSignature)), otherSignature, 'k-')
# plot.plot(threeIndex, threeValuesFiltered)
plot.plot(freq2, sigStren, 'r.')
plot.show()
