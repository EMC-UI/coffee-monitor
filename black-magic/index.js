/**
 * Created by cromed on 8/29/16.
 */
'use strict';

const express = require('express');
let app = express();
const BlackMagic = require('./black-magic');
let blackMagic = new BlackMagic();

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.get('/all', function(req, res) {
    blackMagic.getAll().then((results) => {
        res.json(results);
    })
});

app.get('/hour', function(req, res) {
    blackMagic.getCountByHour().then((results) => {
        res.json(results);
    })
});

app.get('/day', function(req, res) {
    blackMagic.getCountByDay().then((results) => {
        res.json(results);
    })
});

app.get('/start', function(req, res) {
    blackMagic.getStart().then((results) => {
      console.log('got result from start: ', results);
        res.send(results);
    })
});

app.get('/end', function(req, res) {
    blackMagic.getEnd().then((results) => {
      console.log('got result from end: ', results);
        res.send(results);
    })
});

app.listen(3000, function () {
    console.log('Example app listening on port 3000!');
});

app.use(express.static('.'));

