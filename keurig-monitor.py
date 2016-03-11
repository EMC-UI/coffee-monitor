#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

Keurig coffee monitor.  Measure the usage of a keurig coffee maker by monitoring the arm movement
with an accelerometer

Usage:
    keurig-monitor.py [--verbose]  [--record]

Arguments:

Options:
    --verbose               lots of logging
    --record                record the x,y,z movement to a .csv file
    --help                  you're looking at it
    --sampleWindowSec       When monitoring, the number of seconds in which to look for the downward arm movement (default 5)
    --approxXHighPosition   approximate position (in G of the X axis) of the arm in the UP (load) position (default 0.4)
    --approxXLowPosition    approximate position (in G of the X axis) of the arm in the DOWN (brew) position (default 0)
"""

__author__ = 'cp@cjparker.us'

import MPU6050
from docopt import docopt
import math
import time
import numpy
import struct
import requests
import datetime
import pytz

tz = pytz.timezone("America/Denver")

# take this many samples each second
samplesPerSecond = 2

# collect this many total samples
totalSamplesToCollect = 100

# here, we're using the FIFO buffer of the MPU6050, and we'll tell it to
# only count the accelerometer data
bytesPerSample = 6  # accelX, accelY, accelZ

# the MPU6050 can do +/- 2G, 4G, 8G, or 16G where 2G is the most sensitive
accelResolution = 2

# this is how we convert the raw number from the accel into a value
# relative to earth gravity
accelValueToGConversion = float(accelResolution) / 32768.0

# this is how many bytes we can suck out of the MPU6050 FIO at a time
batchSizeBytes = 32.0

# the amount of time to wait for data to accumulate if none is available
secondsToAccum = 1

# prelims
mpu6050 = MPU6050.MPU6050()
mpu6050.setup()
mpu6050.setGResolution(2)

# we only care about movement that happens 5 times a second or slower
mpu6050.setLowPass5Hz()

mpu6050.setSampleRate(samplesPerSecond)

# disable the fifo to start
mpu6050.enableFifo(False)

# wait a spell for the MPU to catch up
time.sleep(0.50)

# now reset
mpu6050.resetFifo()
time.sleep(0.50)

# enable, and capture all the readings
mpu6050.enableFifoAccelOnly(True)
mpu6050.setSampleRate(samplesPerSecond)

cli = docopt(__doc__)


def logIt(message):
    if cli['--verbose']:
        print(message)


def record():
    print(
        'recording at {0} samples per second.  Hit ctrl-c to stop...'.format(samplesPerSecond))

    sampleAccumulator = []
    samplePrintIndex = 0
    outputFile = open("accel-output.csv", "w")
    outputFile.write("Sample,X,Y,Z\n")

    while True:
        bytesAvailable = mpu6050.readFifoCount()

        if bytesAvailable <= 0:
            logIt('no bytes available to read, sleeping for a spell')
            time.sleep(secondsToAccum)
            continue

        if bytesAvailable % bytesPerSample != 0:
            print('continuing because buffer contains a partial sample')
            continue

        else:
            logIt('{0} bytes available'.format(bytesAvailable))

            status = mpu6050.readStatus()

            if status & 0b00010000:
                print("OVERFLOW!!!!! something bad happened")
                exit(1)

            # while there are bytes available to be read, get em
            # put them in sample accumulator
            newByteCounter = 0
            while bytesAvailable > 0:
                bytesToRead = int(batchSizeBytes) if bytesAvailable > int(
                    batchSizeBytes) else bytesAvailable
                sampleAccumulator.extend(mpu6050.readNFromFifo(bytesToRead))
                newByteCounter += bytesToRead
                # print("{0} bytesRead".format(bytesToRead))
                bytesAvailable -= bytesToRead

            logIt('new byte counter is {0}'.format(newByteCounter))
            newSampleCount = newByteCounter / bytesPerSample
            logIt('new samples to print {0}'.format(newSampleCount))
            if newByteCounter % bytesPerSample != 0:
                print('PANIC!!, we read a partial sample!!!')

            # we just read some samples into the sample accum array
            # now dump the samples we just collected to a csv file
            for sampleCount in range(0, newSampleCount):
                start = sampleCount * bytesPerSample + samplePrintIndex
                end = start + bytesPerSample
                sample = sampleAccumulator[start:end]
                rawX = struct.unpack(">h", buffer(bytearray(sample[0:2])))[0]
                rawY = struct.unpack(">h", buffer(bytearray(sample[2:4])))[0]
                rawZ = struct.unpack(">h", buffer(bytearray(sample[4:6])))[0]

                # convert raw values to real gravity numbers
                gravX = rawX * accelValueToGConversion
                gravY = rawY * accelValueToGConversion
                gravZ = rawZ * accelValueToGConversion

                logIt('X:{0:10.10f}, Y:{1:10.10f}, Z:{2:10.10f}'.format(
                    gravX, gravY, gravZ))

                outputFile.write(
                    '{0},{1:10.10f},{2:10.10f},{3:10.10f}\n'.format(samplePrintIndex / bytesPerSample + sampleCount,
                                                                    gravX, gravY,
                                                                    gravZ))
                outputFile.flush()

            samplePrintIndex += newSampleCount * bytesPerSample


# TODO: figure out the exact sample rate1
##
def monitor():
    print('monitoring...')
    sampleWindowSec = cli.get('--sampleWindowSec', 20)
    armHighG = cli.get('--approxXHighPosition', 0.4)
    armLowG = cli.get('--approxXLowPosition', 0.0)
    print('sampleWindowSec:{0} armHighG:{1} armLowG:{2}'.format(
        samplesPerSecond, armHighG, armLowG))

    while True:
        bytesAvailable = mpu6050.readFifoCount()
        logIt('bytes available {0}'.format(bytesAvailable))

        if bytesAvailable < sampleWindowSec * samplesPerSecond * bytesPerSample:
            logIt('need more samples')
            time.sleep(0.1)
            continue

        if bytesAvailable % bytesPerSample != 0:
            print('continuing because buffer contains a partial sample, bytesAvailable : {0}'.format(
                bytesAvailable))
            continue

        status = mpu6050.readStatus()

        if status & 0b00010000:
            print("OVERFLOW!!!!! something bad happened, attempting to recover")

            mpu6050.enableFifo(False)
            time.sleep(0.5)
            mpu6050.resetFifo()
            time.sleep(0.5)
            mpu6050.enableFifoAccelOnly(True)
            continue

        sampleBytes = []
        xSamples = []

        logIt('now processing {0} bytes'.format(bytesAvailable))

        # read the bytes into an array
        newByteCount = bytesAvailable
        while bytesAvailable > 0:
            bytesToRead = int(batchSizeBytes) if bytesAvailable > int(
                batchSizeBytes) else bytesAvailable
            sampleBytes.extend(mpu6050.readNFromFifo(bytesToRead))
            bytesAvailable -= bytesToRead

        # turn the bytes into samples
        newSampleCount = newByteCount / bytesPerSample
        for sampleCount in range(0, newSampleCount):
            start = sampleCount * bytesPerSample
            end = start + bytesPerSample
            sample = sampleBytes[start:end]
            rawX = struct.unpack(">h", buffer(bytearray(sample[0:2])))[0]
            rawY = struct.unpack(">h", buffer(bytearray(sample[2:4])))[0]
            rawZ = struct.unpack(">h", buffer(bytearray(sample[4:6])))[0]

            # convert raw values to real gravity numbers
            gravX = rawX * accelValueToGConversion
            gravY = rawY * accelValueToGConversion
            gravZ = rawZ * accelValueToGConversion
            xSamples.extend([{'g': gravX, 'index': sampleCount}])

        logIt('we have {0} x samples'.format(len(xSamples)))

        # now sort the xSamples and compare the high / low
        sortedX = sorted(xSamples, key=lambda x: x['g'])
        lowX = sortedX[0]
        highX = sortedX[-1]
        logIt('low x: {0:10.10f}, high x:{1:10.10f}'.format(
            lowX['g'], highX['g']))

        if abs(highX['g'] - lowX['g']) >= abs(armHighG - armLowG) and highX['index'] < lowX['index']:
            print("ARM LOWERED!!")
        elif abs(highX['g'] - lowX['g']) >= abs(armHighG - armLowG) and highX['index'] > lowX['index']:
            print("ARM RAISED!!!")


if cli['--record']:
    record()

else:
    monitor()
