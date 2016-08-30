use coffee;
var queryHour = db.getCollection('coffee').aggregate([
    {$match: {action: 'DOWN'}},
    {$group: {
        _id : { hourOfDay: { $hour: '$dateTime'} },
        count: { $sum: 1 }
    }},
    {$sort: { _id : 1}}
]);
queryHour.pretty();

var queryDay = db.getCollection('coffee').aggregate([
    {$match: {action: 'DOWN'}},
    {$group: {
        _id : { dayOfWeek: { $dayOfWeek: "$dateTime" }},
        count: { $sum: 1 }
    }},
    {$sort: { _id: 1}}
]);

queryDay.pretty();