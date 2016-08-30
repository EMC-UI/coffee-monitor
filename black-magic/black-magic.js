/**
 * Created by cromed on 8/29/16.
 */
'use strict';

const pm = require('promised-mongo');
const collection = 'coffee';
let db = pm('mongodb://localhost/coffee');
const moment = require('moment');


class BlackMagic {

    constructor() {
        //
    }

    getCollection() {
        return db.collection(collection);
    }

    getAll() {
        return this.getCollection().find();
    }

    getLevers(which) {
        return this.getCollection().find({action:which});
    }
    getCount(filter) {
        return this.getCollection().count(filter);
    }

    getStart() {
        return this.getCollection().find({}).sort('dateTime',-1);
    }

    getEnd() {
        return this.getCollection().find({}).sort('dateTime',1);
    }

    fillHours(results) {
      var fill = [...Array(24).keys()];
      var filled = fill.map((num) => {
        var found = results.find((res) => {
          return (num === res._id.hourOfDay);
        });
        console.log('found?: ', found);
        if (!found) {
          return {
            _id: {
              hourOfDay:num,
            },
            count: 0
          }
        } else {
          return found;
        }
      });
      return filled.map((result) => {
        result.hourOfDay = result._id.hourOfDay;
        console.log('mapping', result);
        result.label = moment().hour(result.hourOfDay).minute(0).format('hh:mm a');
        console.log('result: ', result);
        return result;
      });
    }

    getCountByHour() {
        return this.getCollection().aggregate(
            {$match: {action: 'DOWN'}},
            {$group: {
                _id : { hourOfDay: { $hour: '$dateTime'} },
                count: { $sum: 1 }
            }},
            {$sort: { _id : 1}}
        ).then(this.fillHours);
    }

    getCountByDay() {
        return this.getCollection().aggregate(
            {$match: {action: 'DOWN'}},
            {$group: {
                _id : { dayOfWeek: { $dayOfWeek: "$dateTime" }},
                count: { $sum: 1 }
            }},
            {$sort: { _id: 1}}
        );
    }

}

module.exports = BlackMagic;
