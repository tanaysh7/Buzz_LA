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

client.search({
  index: 'event',
  type: 'events',
  body: {
    query: {
      bool: {
        should: [
          { match: { title: 'artificial intelligence research talk' } },
          { match: { description: 'artificial intelligence research talk' } }
        ]
      }
    }
  }
}).then(function (resp) {
    var hits = resp.hits.hits;
    hits.forEach(function (element) {
      //Fill the table
      var title = element._source.title;
      var link = element._source.link;
      var desc = element._source.description;
      var location = element._source.location;
      var univ = element._source.univ;
      var _time = element._source.time;
      console.log(title);
    });
   }, function (err) {
        console.trace(err.message);
      });
