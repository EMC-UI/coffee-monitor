/**
 * Created by cromed on 8/29/16.
 */
'use strict';

const pm = require('promised-mongo');
const collection = 'coffee';
let db = pm('mongodb://localhost/coffee');


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

    getCountByHour() {
        return this.getCollection().aggregate(
            {$match: {action: 'DOWN'}},
            {$group: {
                _id : { hourOfDay: { $hour: '$dateTime'} },
                count: { $sum: 1 }
            }},
            {$sort: { _id : 1}}
        );
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
