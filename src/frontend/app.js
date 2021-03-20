// app.js
let express = require('express');
let app = express();

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
    res.render('home')
});

// Setup route
app.get('/setup', function (req, res) {
    const newsCategories = [
        'Business',
        'Entertainment',
        'General',
        'Health',
        'Science',
        'Sports',
        'Technology'
    ]

    const newsSources = [
        'ABC News',
        'Al Jazeera English',
        'Ars Technica',
        'Associated Press',
        'Australian Financial Review',
        'Axios',
        'BBC News',
        'BBC Sport',
        'Bleacher Report',
        'Bloomberg',
        'Breitbart News',
        'Business Insider',
        'Business Insider (UK)',
        'Buzzfeed',
        'CBS News',
        'CNN',
        'Crypto Coins News',
        'Endgadget',
        'Entertainment Weekly',
        'ESPN',
        'ESPN Cric Info'
    ]

    res.render('setup', {
        newsCategories: newsCategories,
        newsSources: newsSources
    })
});

// Let node listen to port 8080
app.listen(PORT, HOST, function () {
    console.log(`Running on http://${HOST}:${PORT}`);
});
