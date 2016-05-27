#!/usr/bin/env node
'use strict'


const fs = require('fs')
const pm = require('promised-mongo')
const moment = require('moment')
const _ = require('underscore')
const Await = require('asyncawait/await')
const Async = require('asyncawait/async')

let db = pm('mongodb://localhost/coffee')



let doIt = Async(() => {
  let data = JSON.parse(fs.readFileSync('data.json','utf-8'))
  _.each(data, record => {
    var realDate = moment(record.dateTime)
    record.dateTime = realDate.toDate()

    let result = Await(db.collection('coffee').insert(record)
      .then(() => {
        process.stdout.write('.')
      })
      .catch((er) => {
         console.log('caught error',er)
      }))
  })
  console.log('done')
  db.close()
})


doIt()



