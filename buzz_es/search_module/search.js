var elasticsearch = require('elasticsearch'); 
var client = new elasticsearch.Client({ host: 'localhost:9200', log: 'trace' });


module.exports.search = function (searchData, callback) {
 
    var search_query = 'artificial intelligence research talk'; // space separated query (required field)
var univ_name = 'USC UCLA CALTECH CALSTATE'; //space separated university name
var _tags = 'Alumni Art Career Dance_Theatre_Film Lecture_Talk_Workshop Music Social Student Wellness'; // single tag
var date_gte = "2019-04-01"; //start date format: "yyyy-mm-dd" [REQUIRED]
var date_lte = "2019-12-31"; //end date format: "yyyy-mm-dd" [REQUIRED]
// var promise = client.ping();

// promise.then(function (response) {
//   console.log("response " + response);},
// function (error) {
//   console.error('elasticsearch cluster is down!');
// });

     client.search({index: 'event',
     type: 'events',
     body: {
       query: {
         bool: {
           must: [
             { match: { title: searchData.searchTerm } }, //matches both description and title, as desc = desc + title
             { match: { univ: univ_name } },
             { match: { tags: _tags } }
           ],
           filter: {
             range: {
               "date_time.date": {
                 gte: date_gte,
                 lte: date_lte,
                 // format: "yyyy-mm-dd"
               }
             }
           }
         }
       },
       sort: [
         { "date_time.date": "asc" } //sorted by date
       ]
     }
   }
                           
                           
                           
).then(function (resp) { var hits = resp.hits.hits;
     callback(hits); }, function (err) {
          callback(err.message) 
          console.trace(err.message); }); 
} 