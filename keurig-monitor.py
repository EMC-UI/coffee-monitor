#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

Keurig coffee monitor.  Measure the usage of a keurig coffee maker by monitoring the arm movement
with an accelerometer

Usage:
    keurig-monitor.py [--verbose]  [--record]

Arguments:

Options:
    --verbose                       lots of logging
    --record                        record the x,y,z movement to a .csv file
    --help                          you're looking at it
    --sampleWindowSec=<swc>         When monitoring, the number of seconds in which to look for the downward arm movement [default: 5]
    --approxXHighPosition=<xhigh>   approximate position (in G of the X axis) of the arm in the UP (load) position [default: 0.50]
    --approxXLowPosition=<xlow>     approximate position (in G of the X axis) of the arm in the DOWN (brew) position [default: 0.03]
    --XPositionDelta=<delta>        fudge factor (in G) to use when looking for the X high and low positions [default: 0.1]
"""

import struct
import time
import numpy as np
from docopt import docopt
import MPU6050
import pytz
import datetime
import json
__author__ = 'cp@cjparker.us'

dataFilePath = '/opt/coffee-monitor/data.json'

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
print cli


def logIt(message):
    if cli['--verbose']:
        print message


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
            print 'continuing because buffer contains a partial sample'
            continue

        else:
            logIt('{0} bytes available'.format(bytesAvailable))

            status = mpu6050.readStatus()

            if status & 0b00010000:
                print "OVERFLOW!!!!! something bad happened"
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
                print 'PANIC!!, we read a partial sample!!!'

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
    print 'monitoring...'
    armHighG = cli.get('--approxXHighPosition', 0.50)
    armLowG = cli.get('--approxXLowPosition', 0.03)
    positionDelta = cli.get('--XPositionDelta', 0.1)
    print('sampleWindowSec:{0} armHighG:{1} armLowG:{2}, XPositionDelta:{3}'.format(
        samplesPerSecond, armHighG, armLowG, positionDelta))

    # open the data file
    dataFile = open(dataFilePath, 'a')

    lastXPos = 0
    while True:
        sampleBytes = []
        xSamples = []
        bytesAvailable = mpu6050.readFifoCount()

        if bytesAvailable <= 0:
            time.sleep(1)
            continue

        saveBytesAvail = bytesAvailable
        while bytesAvailable > 0:
            bytesToRead = int(batchSizeBytes) if bytesAvailable > int(
                batchSizeBytes) else bytesAvailable
            sampleBytes.extend(mpu6050.readNFromFifo(bytesToRead))
            bytesAvailable -= bytesToRead

        logIt('Just read {0} bytes'.format(saveBytesAvail))
        newSampleCount = len(sampleBytes) / bytesPerSample
        for sampleCount in range(0, newSampleCount - 1):
            start = sampleCount * bytesPerSample
            end = start + bytesPerSample
            sample = sampleBytes[start:end]
            rawX = struct.unpack(">h", buffer(bytearray(sample[0:2])))[0]
            # convert raw values to real gravity numbers
            gravX = rawX * accelValueToGConversion
            xSamples.extend([gravX])

        # take average x position
        newXPos = np.average(np.array(xSamples))
        logIt('new x pos {0}'.format(newXPos))
        if (lastXPos - positionDelta) <= newXPos <= (lastXPos + positionDelta):
            logIt('arm has not moved')
        else:
            logIt('arm is in new position')
            if (armLowG - positionDelta) <= newXPos <= (armLowG + positionDelta):
                print 'arm has moved DOWN'
                rec = {
                    'dateTime': datetime.datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S%z'),
                    'action' : 'DOWN'
                }
                json.dump(rec, dataFile)
                dataFile.flush()
            elif (armHighG - positionDelta) <= newXPos <= (armHighG + positionDelta):
                print 'arm has moved UP'
                rec = {
                    'dateTime': datetime.datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S%z'),
                    'action' : 'UP'
                }
                json.dump(rec, dataFile)
                dataFile.flush()
            else:
                print 'error, arm is in an unknown position {0}'.format(newXPos)

        lastXPos = newXPos

        time.sleep(1)


if cli['--record']:
    record()

else:
    monitor()
