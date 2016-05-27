#!/usr/bin/env node
'use strict'

const _ = require('underscore')
const pm = require('promised-mongo')
const moment = require('moment')

let db = pm('mongodb://localhost/coffee')


db.collection('coffee').find()
  .then(data => {

    // get only the down events
    let downs = _.filter(data, record => {
      return record.action.toLowerCase() == 'down'
    })

    let dayGroups = _.groupBy(downs, d => {
      let m = moment(d.dateTime)
      return m.format('ddd')
    })

    let hourGroups = _.groupBy(downs, d => {
      let m = moment(d.dateTime)
      return m.format('HH')
    })

    let byDay = _.mapObject(dayGroups, (val,key) => {
      return val.length
    })

    let byHour = _.mapObject(hourGroups, (val,key) => {
      return val.length
    })


    let sorted = _.sortBy(_.pairs(byDay), pair => {
      return pair[1]
    }).reverse()

    let formatted = _.map(sorted, pair => {
      let x = {}
      x[pair[0]] = pair[1]
      return x
    })

    let hourSorted = _.sortBy(_.pairs(byHour), pair => {
      return pair[1]
    }).reverse()

    let hourFormatted = _.map(hourSorted, pair => {
      let x = {}
      x[pair[0]] = pair[1]
      return x
    })

    console.log(hourFormatted)
    db.close()

  })
