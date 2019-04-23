var elasticsearch = require('elasticsearch');
var client = new elasticsearch.Client ({
  host: 'localhost:9200',
  log: 'trace'
});

var promise = client.ping();

promise.then(function (response) {
  console.log("response " + response);},
function (error) {
  console.error('elasticsearch cluster is down!');
});

var search_query = 'artificial intelligence research talk'; // space separated query (required field)
var univ_name = 'USC CALTECH CALSTATE'; //space separated university name
var _tags = 'Lecture_Talk_Workshop'; // single tag
var date_gte = "2019-04-01"; //start date format: "yyyy-mm-dd" [REQUIRED]
var date_lte = "2019-12-31"; //end date format: "yyyy-mm-dd" [REQUIRED]

//If user does not give input
if (search_query == ''){ search_query = "the"}
if (univ_name == ''){ univ_name = "USC UCLA CALTECH CALSTATE"}
if (_tags == ''){ _tags = 'Alumni Art Career Dance_Theatre_Film Lecture_Talk_Workshop Music Social Student Wellness'}

client.search({
  index: 'event',
  type: 'events',
  body: {
    query: {
      bool: {
        must: [
          { match: { description: search_query } }, //matches both description and title, as desc = desc + title
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
}).then(function (resp) {
    var hits = resp.hits.hits;
    hits.forEach(function (element) {
      //Fill the table using these fields
      var title = element._source.title;
      var link = element._source.link;
      var desc = element._source.description;
      var location = element._source.location;
      var univ = element._source.univ;
      var _time = element._source.date_time.time;
    });
   }, function (err) {
        console.trace(err.message);
      });
