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
            // TODO: implement imperial
            weatherLocation.innerText = response.response['city_name'];
            temperature.innerText = `${Math.round(response.response.weather.temp['current'])} °C`;
            weatherType.innerText = capitalizeFirstLetter(response.response.weather['description']);
            windType.innerText = `Wind: ${response.response.weather.wind.speed} m/s Moderate breeze`;
            weatherImage.src = `http://openweathermap.org/img/wn/${response.response.weather.icon}@2x.png`;
        },
        error: function (error) {
            console.log(error)
        }
    })
}

function retrieveWeatherInformationForTheNight() {

    $.ajax({
        url: 'http://localhost:5600/rest/api/v1/dialogflow/query',
        type: 'POST',
        data: JSON.stringify({
            'message': "Whats the weather for the next 7 days?"
        }),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        success: function (response) {
            let html = createWeatherForecast(response);
            document.getElementById('weatherGoodBye').appendChild(html);

        },
        error: function (error) {
            console.log(error)
        }
    })

}

/**
 *
 * @param weather
 * @returns {HTMLDivElement}
 */
function createWeatherForecast(weather) {

    let response = weather.response;

    console.log(response)

    let html = `<h1 class="dark:text-gray-300 font-light">Weather forecast for ${response.city_name}</h1>
                    <div class="h-0.5 dark:bg-gray-300 dark:bg-opacity-25 rounded my-1"></div>
                    <div class="flex">
                        ${handleMultipleWeatherData(response.weather)}
                    </div>`;

    let div = document.createElement('div');
    div.classList.add('bg-gray-700', 'bg-opacity-40', 'p-2', 'rounded-lg');

    div.innerHTML = html;

    console.log(div)

    return div;
}


function setHeader(xhr) {
    xhr.setRequestHeader('Access-Control-Allow-Headers', 'access-control-allow-methods, access-control-allow-origin');
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE');
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}



