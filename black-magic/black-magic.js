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
        return this.getCollection().find({action:'DOWN'}).sort({dateTime:-1}).limit(1).then(result => moment(result[0].dateTime).format("dddd, MMMM Do YYYY"));
    }

    getEnd() {
        return this.getCollection().find({action:'DOWN'}).sort({dateTime:1}).limit(1).then(result => moment(result[0].dateTime).format("dddd, MMMM Do YYYY"));
    }

    fillHours(results) {
      var fill = [...Array(24).keys()];
      var filled = fill.map((num) => {
        var found = results.find((res) => {
          return (num === res._id.hourOfDay);
        });
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
        result.hour = result._id.hourOfDay;
        result.label = moment().hour(result.hour).minute(0).format('hh:mm a');
        delete result._id;
        return result;
      });
    }

    fixDays(results) {
      return results.map((result) => {
        result.day = result._id.dayOfWeek;
        result.label = moment().day(result.day-1).format('dddd');
        delete result._id;
        return result;
      })
    }

    getCountByHour() {
        return this.getCollection().aggregate(
            {$match: {action: 'DOWN'}},
            {$group: {
                _id : { hourOfDay: { $hour: '$dateTime'} },
                count: { $sum: 1 }
            }},
            {$sort: { _id : -1}}
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
        ).then(this.fixDays);
    }

}

module.exports = BlackMagic;
