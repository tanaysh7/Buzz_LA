var elasticsearch = require('elasticsearch'); 
var client = new elasticsearch.Client({ host: 'localhost:9200', log: 'trace' });


module.exports.search = function (searchData, callback) {
 
    if (searchData.searchTerm=='') 
    var searchterm = 'the of in to Alumni :';
    else
    var searchterm=searchData.searchTerm; // space separated query (required field)

    if (searchData.tags=='All')
    var _tags = 'Alumni Art Career Dance_Theatre_Film Lecture_Talk_Workshop Music Social Student Wellness';
    else
    var _tags = searchData.tags;
    

   
    
    
    var univ_name=''
    if (Array.isArray(searchData.school)){
var arrayLength = searchData.school.length;
    for (var i = 0; i < arrayLength; i++) {
        univ_name+=' '+searchData.school[i]   
    }
  }
  else
  univ_name=searchData.school

  if (!univ_name)
var univ_name='USC UCLA CALTECH CALSTATE'; //space separated university name
 // single tag
var date_gte = searchData.start_date;//"2019-04-01"; //start date format: "yyyy-mm-dd" [REQUIRED]
var date_lte = "2019-12-31"; //end date format: "yyyy-mm-dd" [REQUIRED]
// var promise = client.ping();
if(!date_gte)
date_gte="2019-04-01"

if(date_gte=="")
date_gte="2019-04-01"


     client.search({index: 'event',
     type: 'events',
     body: {
       query: {
         bool: {
           must: [
             { match: { title: searchterm } }, //matches both description and title, as desc = desc + title
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