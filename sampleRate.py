#!/usr/bin/python
# -*- coding: utf-8 -*-


# Let's startup, set sample rate low and turn on LPF
# infinite loop that gets available byte count, reads bytes, sleeps
# for 1 sec, then loops

import timeit
import MPU6050
import time
import sys

mpu6050 = MPU6050.MPU6050()
mpu6050.setup()
mpu6050.setGResolution(2)



print('sample rate is {0}'.format(sys.argv[1]))
x = int(sys.argv[1])
print('x is {0}'.format(x))
mpu6050.enableFifo(False)
time.sleep(0.5)

mpu6050.resetFifo()
mpu6050.resetFifo()
mpu6050.setLowPass5Hz()
mpu6050.setSampleRateWithDLP(x)
time.sleep(0.5)

batchSizeBytes = 32

mpu6050.enableFifoAccelOnly(True)  # 6 bytes per sample


while True:
    bytesAvailable = mpu6050.readFifoCount()
    saveBytesAvail = bytesAvailable
    while bytesAvailable > 0:
        bytesToRead = int(batchSizeBytes) if bytesAvailable > int(batchSizeBytes) else bytesAvailable
        mpu6050.readNFromFifo(bytesToRead)
        bytesAvailable -= bytesToRead

    print('Just read {0} bytes'.format(saveBytesAvail))
    time.sleep(1)
