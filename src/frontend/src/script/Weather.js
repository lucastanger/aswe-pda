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
        type: 'POST',
        data: JSON.stringify({
            'message': "What's the weather today?"
        }),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        success: function (response) {

            console.log(response.response);
            // TODO: implement imperial
            weatherLocation.innerText = response.response['city_name'];
            temperature.innerText = `${Math.round(response.response.weather.temp['current'])} °C`;
            weatherType.innerText = capitalizeFirstLetter(response.response.weather['description']);
            windType.innerText = `Wind: ${response.response.weather.wind.speed} m/s Moderate breeze`;

            // TODO: implement dynamic image
            weatherImage.src = 'icons/regen.svg';
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

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}



