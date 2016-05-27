Keurig Coffee Monitor
=====================

Monitoring the use of a [Keurig](http://goo.gl/837jcJ) coffee machine using an [mpu-6050](http://goo.gl/KCvR5r) accelerometer and a [raspberry pi](https://www.raspberrypi.org/products/model-b-plus/)

The accelerometer is connected to the raspberry pi like this:

![wiring](https://raw.githubusercontent.com/EMC-UI/coffee-monitor/master/block-diagram.png)

The accelerometer samples the position of the Keurig 'arm' 20 times a second.  

Here are time plots of the accelerometer X, Y, and Z values while raising and lowering the arm:

![raising](https://raw.githubusercontent.com/EMC-UI/coffee-monitor/master/raise-arm.png)

![lowering](https://raw.githubusercontent.com/EMC-UI/coffee-monitor/master/lower-arm.png)

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

## MongoDB data
There is a mongo DB dump included in this repo.  To import it into mongo:

```
mongorestore coffee-dump-mongo
```

The DB name is `coffee` and the collection name is also `coffee`

