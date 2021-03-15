// app.js
var express = require('express');
var app = express();

const PORT = 8080;
const HOST = '0.0.0.0';


// Define internal routes
app.use(express.static(__dirname + '/src'));
app.set('views', __dirname + '/src/views');
app.set('img', __dirname + 'src/img');
app.set('script', __dirname + 'src/script');
app.set('icons', __dirname + 'src/icons');

// Set view engine to ejs
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'ejs');

// Home route
app.get('/', function (req, res) {
    res.render('home.html')
});

// Setup route
app.get('/setup', function (req, res) {
    res.render('setup.html')
});

// Let node listen to port 8080
app.listen(PORT, HOST, function () {
    console.log(`Running on http://${HOST}:${PORT}`);
});
