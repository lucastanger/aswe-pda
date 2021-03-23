// Weather.js
let weatherLocation, temperature, weatherType, windType, weatherImage;

// If document is ready, get control over DOM Elements
$(document).ready(function () {
    weatherLocation = document.getElementById('weather-location');
    temperature = document.getElementById('temperature');
    weatherType = document.getElementById('weather-type');
    windType = document.getElementById('wind-type');
    weatherImage = document.getElementById('weather-image');

    retrieveWeatherInformationForTheDay();
});

// Get Information about todays weather
function retrieveWeatherInformationForTheDay() {

    $.ajax({
        url: 'http://localhost:5600/rest/api/v1/dialogflow/query',
        type: 'GET',
        data: JSON.stringify({
            'message': "What's the current weather"
        }),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        success: function (response) {

            weatherLocation.innerText = "";
            temperature.innerText = "";
            weatherType.innerText = "";
            windType.innerText = "";

        },
        error: function (error) {
            console.log(error)
        }
    })

}



