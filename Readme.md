Keurig Coffee Monitor
=====================

## Accessing the data

The data is available in a mongo database running on the internal EMC network.  Use the following mongodb URL to access the data:

```
mongodb://128.222.174.194/coffee
```

The collection name is **coffee**

**For example** browse the data with your mongo client on the command line like so:
```
mongo mongodb://128.222.174.194/coffee
> use coffee
switched to db coffee
> db.coffee.count()
2683
> db.coffee.findOne()
{
        "_id" : ObjectId("57486c1e5ebcd5faa97f8d29"),
        "action" : "UP",
        "dateTime" : ISODate("2016-03-23T02:56:06Z")
}
>
```

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

**UP** means the keurig arm went up.
**DOWN** means the keurig arm went down.  
**dateTime** is in [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) format

[Here](https://www.mongodb.com/download-center#community) are instructions for **downloading and installing the mongo DB server and client**

If you want to import the raw data into your own mongo database, a dump of the data named coffee-dump-mongo is available in the git repo.

```
mongorestore coffee-dump-mongo
```

The DB name is `coffee` and the collection name is also `coffee`




## How the monitor works

Monitoring the use of a [Keurig](http://goo.gl/837jcJ) coffee machine using an [mpu-6050](http://goo.gl/KCvR5r) accelerometer and a [raspberry pi](https://www.raspberrypi.org/products/model-b-plus/)

The accelerometer is connected to the raspberry pi like this:

![wiring](https://raw.githubusercontent.com/EMC-UI/coffee-monitor/master/block-diagram.png)

The accelerometer samples the position of the Keurig 'arm' 20 times a second.  

Here are time plots of the accelerometer X, Y, and Z values while raising and lowering the arm:

![raising](https://raw.githubusercontent.com/EMC-UI/coffee-monitor/master/raise-arm.png)

![lowering](https://raw.githubusercontent.com/EMC-UI/coffee-monitor/master/lower-arm.png)

The keurig-monitor.py code watches for changes in the arm position.  When the arm moves to its 'high' and 'low' positions the event is logged, with a time stamp, to a .json text file and saved to the SD card.


## Example Analysis
As of Friday, May 27, 2016, here is our coffee consumption by hour:

```
[ { '09': 300 },
  { '08': 265 },
  { '10': 188 },
  { '14': 116 },
  { '11': 111 },
  { '13': 92 },
  { '15': 86 },
  { '12': 72 },
  { '16': 54 },
  { '07': 31 },
  { '17': 17 },
  { '18': 7 },
  { '23': 2 },
  { '20': 2 },
  { '05': 1 },
  { '00': 1 },
  { '06': 1 },
  { '04': 1 },
  { '03': 1 },
  { '19': 1 } ]
```


# Black Magic - putting a UI on the coffee data.

## Another way to get the munged data into the db
tar -xvf coffee-db.tar
mongorestore

## Run the rest server
node black-magic/index.js

## Run the UI ( requires angular-cli installed )
ng serve

## Open browser to http://localhost:4200
