Keurig Coffee Monitor
=====================

Monitoring the use of a [Keurig](http://goo.gl/837jcJ) coffee machine using an [mpu-6050](http://goo.gl/KCvR5r) accelerometer and a [raspberry pi](https://www.raspberrypi.org/products/model-b-plus/)

The accelerometer is connected to the raspberry pi like this:

![wiring]()

The accelerometer samples the position of the Keurig 'arm' 20 times a second.  

Here are time plots of the accelerometer X, Y, and Z values while raising and lowering the arm:

![raising]()

![lowering]()

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
