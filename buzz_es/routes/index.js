var express = require('express');
var router = express.Router();
var searchModule=require('../search_module/search');
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Buzz LA' });
});

router.post('/search-results',function(req,res){
  // alert(req);

searchModule.search(req.body, function(data) { 

      res.render('index', { title: 'Buzz LA', results: data }); 
      }); 
    });

module.exports = router;
