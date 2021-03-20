function generateConfig() {
    let conf = new ConfigGenerator();
    console.log(JSON.stringify(conf));
    sendConfiguration(conf)
}


function sendConfiguration(configuration) {
    $.ajax({
        url: 'http://localhost:5600/rest/api/v1/configuration/',
        type: 'POST',
        data: JSON.stringify(configuration),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        success: function (response) {
            console.log(response)
        },
        error: function (error) {
            console.log(error)
        }

    })
}

function setHeader(xhr) {
    xhr.setRequestHeader('Access-Control-Allow-Headers', 'access-control-allow-methods, access-control-allow-origin');
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE');
}


class ConfigGenerator {

    // Ctor
    constructor() {
        this.general = new General(
            document.getElementById('name').value
        );
        this.dualis = new DualisServiceConfig(
            document.getElementById('dualisMail').value,
            document.getElementById('dualisPW').value
        );
        this.news = new NewsServiceConfiguration(
            document.getElementById('newspaper').value,
            getNewsCategories()
        );
        this.weather = new WeatherServiceConfiguration(
            new Location(
                12.4,
                14.6
            ),
            getWeatherUnit()
        );
        this.stocks = new StocksServiceConfiguration(
            document.getElementById('selectedStock').innerText
        );
    }

}

function getWeatherUnit() {
    let rbs = document.getElementsByName('weatherRadio');
    let checked = "metric";

    rbs.forEach((entry) => {
        if (entry.checked) {
            checked = entry.id;
        }
    })

    return checked;
}

function getNewsCategories() {
    let cbs = document.getElementsByName('newsCategory');
    let checked = [];

    for (let cb of cbs) {
        if (cb.checked) {
            checked.push(cb.id);
        }
    }

    return checked;
}

class General {

    constructor(username, welcomeTime = "09:00:00", goodbyeTime = "21:00:00") {
        this._username = username;
        this._welcomeTime = welcomeTime;
        this._goodbyeTime = goodbyeTime;
    }

    get username() {
        return this._username;
    }

    set username(value) {
        this._username = value;
    }

    get welcomeTime() {
        return this._welcomeTime;
    }

    set welcomeTime(value) {
        this._welcomeTime = value;
    }

    get goodbyeTime() {
        return this._goodbyeTime;
    }

    set goodbyeTime(value) {
        this._goodbyeTime = value;
    }
}

class DualisServiceConfig {

    constructor(username, password) {
        this._username = username;
        this._password = password;
    }

    get username() {
        return this._username;
    }

    set username(value) {
        this._username = value;
    }

    get password() {
        return this._password;
    }

    set password(value) {
        this._password = value;
    }
}

class NewsServiceConfiguration {

    constructor(papers, categories) {
        this._papers = papers;
        this._categories = categories;
    }

    get papers() {
        return this._papers;
    }

    set papers(value) {
        this._papers = value;
    }

    get categories() {
        return this._categories;
    }

    set categories(value) {
        this._categories = value;
    }
}

class WeatherServiceConfiguration {

    constructor(location, unit) {
        this._location = location;
        this._unit = unit;
    }

    get location() {
        return this._location;
    }

    set location(value) {
        this._location = value;
    }

    get unit() {
        return this._unit;
    }

    set unit(value) {
        this._unit = value;
    }
}

class Location {

    constructor(lat, lon) {
        this._lat = lat;
        this._lon = lon;
    }

    get lat() {
        return this._lat;
    }

    set lat(value) {
        this._lat = value;
    }

    get lon() {
        return this._lon;
    }

    set lon(value) {
        this._lon = value;
    }
}

class StocksServiceConfiguration {

    constructor(stock) {
        this._stock = stock;
    }

    get stock() {
        return this._stock;
    }

    set stock(value) {
        this._stock = value;
    }
}
