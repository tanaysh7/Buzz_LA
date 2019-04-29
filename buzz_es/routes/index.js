var express = require('express');
var router = express.Router();
var searchModule=require('../search_module/search');
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Buzz LA' });
});

router.get('/buzz-cloud', function(req, res, next) {
  searchModule.cloud(req.body, function(data) { 
    res.render('cloud', { title: 'Buzz LA', results: data }); 
    }); 
  });



router.post('/search-results',function(req,res){
 

searchModule.search(req.body, function(data) { 

      res.render('index', { title: 'Buzz LA', results: data }); 
      }); 
    });

module.exports = router;
