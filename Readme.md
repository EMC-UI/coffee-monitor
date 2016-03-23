Keurig Coffee Monitor
=====================

Monitoring the use of a [Keurig](http://goo.gl/837jcJ) coffee machine using an [mpu-6050](http://goo.gl/KCvR5r) accelerometer and a [raspberry pi](https://www.raspberrypi.org/products/model-b-plus/)

The accelerometer is connected to the raspberry pi like this:

![wiring](http://ucas-stash.lss.emc.com/projects/EM/repos/coffee-monitor/browse/block-diagram.png?at=cbad10952850e2fd1f33975575751d4ec3aaf1ce&raw)

The accelerometer samples the position of the Keurig 'arm' 20 times a second.  

Here are time plots of the accelerometer X, Y, and Z values while raising and lowering the arm:

![raising](http://ucas-stash.lss.emc.com/projects/EM/repos/coffee-monitor/browse/raise-arm.png?at=cbad10952850e2fd1f33975575751d4ec3aaf1ce&raw)

![lowering](http://ucas-stash.lss.emc.com/projects/EM/repos/coffee-monitor/browse/lower-arm.png?at=cbad10952850e2fd1f33975575751d4ec3aaf1ce&raw)

The keurig-monitor.py code watches for changes in the arm position.  When the arm moves to its 'high' and 'low' positions the event is logged, with a time stamp, to a .json text file and saved to the SD card.

The JSON data looks like this:


```
[
    {
        "action": "UP",
        "dateTime": "2016-03-22T20:56:06-0600"
    },
    {
        "action": "DOWN",
        "dateTime": "2016-03-22T20:59:37-0600"
    },
    {
        "action": "UP",
        "dateTime": "2016-03-22T20:59:46-0600"
    }
]
```
