// Chat.js
const input = document.getElementById('chatInput');
const chatArea = document.getElementById('chatArea');
const headerInput = document.getElementById('headerChatInput');

// Globals
let data = "";
let uuid = "";
let stockTitle = "";
let grades = {};
let mapData;

let weekday = new Array(7);
weekday[0] = "Sun";
weekday[1] = "Mon";
weekday[2] = "Tue";
weekday[3] = "Wed";
weekday[4] = "Thu";
weekday[5] = "Fri";
weekday[6] = "Sat";


$(document).ready(function () {
    // Add Event listener for Bottom input bar
    input.addEventListener("keyup", function (event) {
        if (event.code === 'Enter') {
            event.preventDefault()
            // Send the message
            sendMessage(input).then(function (r) {
                console.log(r)
            });
        }
    });
    // Add Event listener for Top input bar
    headerInput.addEventListener("keyup", function (event) {
        if (event.code === 'Enter') {
            event.preventDefault()
            // Load chat page
            loadPage('chat');
            // Toggle chat button
            toggleButton(document.getElementsByName('chat')[0]);
            // Send the message
            sendMessage(headerInput).then(function (r) {
                console.log(r)
            });

        }
    })
});

/**
 *
 * @returns {Promise<void>}
 */
async function sendMessage(from) {
    // Retrieve user message
    let chatMessage = from.value;
    // Delete user input
    from.value = "";
    // Log user input for debug purposes
    //console.log(chatMessage);
    // Display Chat Message
    let chatElement = createChatElement(chatMessage);
    chatArea.appendChild(chatElement);

    // Special response if a module got selected
    if (chatMessage.startsWith("Module:")) {

        let selectedModule = chatMessage.replace("Module:", "")

        chatArea.appendChild(createGradeReport(selectedModule));

        return;
    }

    sendMessageToMiddleware(chatMessage).then(function (res) {

        // Play Sound
        new Audio("data:audio/wav;base64," + res.dialogflow.output_audio).play()

        let intentFunction = identifyIntent(res)

        let answerElement = intentFunction(res);

        chatArea.appendChild(answerElement);

        // If it is a stock intent
        if (intentFunction === handleStockIntent) {
            createStockPlot(data, uuid, stockTitle);
        }

        if (intentFunction === handleMapsIntent) {
            drawMap(uuid);
            calcRoute();
        }

    });

}

/**
 * Returns the proper function according to intent type
 * @param intent
 * @returns {(function(*): (boolean|HTMLDivElement))|(function(): string)|(function(*): HTMLDivElement)}
 */
function identifyIntent(intent) {

    // Create a UUID for the request
    uuid = uuidv4();

    switch (intent.dialogflow.query_result.intent.display_name) {
        case 'weather-intent':
            return handleWeatherIntent;
        case 'spotify-intent':
            return handleSpotifyIntent;
        case 'news-intent':
            return handleNewsIntent;
        case 'calendar-intent':
            return handleCalendarIntent;
        case 'stock-intent':
            return handleStockIntent;
        case 'dualis-intent':
            return handleDualisIntent;
        case 'maps-intent':
            return handleMapsIntent;
        default:
            // If intent could not get identified
            return () => {return `${intent.dialogflow.query_result.intent.display_name} does not have a according intent function`}
    }
}

/**
 *
 * @param {Array} weather
 */
function handleMultipleWeatherData(weather) {

    let ret = "";

    weather.forEach(element => {

        ret += `<div class="px-5">
                            <p class="dark:text-gray-100 font-light text-xl">${weekday[new Date(element.time.dt * 1000).getDay()]}, ${new Date(element.time.dt * 1000).getDate()}.${new Date(element.time.dt * 1000).getUTCMonth() + 1}</p>
                            <div class="flex items-center">
                                <img class="h-24" src="http://openweathermap.org/img/wn/${element.icon}@2x.png" alt="rain" id="weather-image">
                                <p class="dark:text-gray-100 font-normal" id="temperature">${Math.round(element.temp.day)}°C</p>
                            </div>
                            <div class="col-span-full flex flex-col pt-5">
                                <p class="dark:text-gray-100 font-normal text-xl" id="weather-type">${element.description}</p>
                                <p class="dark:text-gray-500" id="wind-type">Wind: ${element.wind.speed} m/s</p>
                                <p class="dark:text-gray-500" id="wind-type">Direction: ${element.wind.deg}°</p>
                                <p class="dark:text-gray-500" id="wind-type">Max Temp: ${element.temp.max}</p>
                                <p class="dark:text-gray-500" id="wind-type">Min Temp: ${element.temp.min}</p>
                                <p class="dark:text-gray-500" id="wind-type">Feels Like: ${element.temp.feels_like.day}</p>
                            </div>
                        </div>`;

    });

    return ret;

}

function createGradeReport(selectedModule) {

    let module = grades[selectedModule];
    let html = `<h1>${module.id}</h1>`;
    let textToSpeech = "Your grade is ";

    module.forEach(singleModule => {

        if (singleModule.hasOwnProperty('name') && singleModule.hasOwnProperty('grade')) {
            html += `<p>${singleModule.name}: ${singleModule.grade}</p>`;
            textToSpeech += `${singleModule.grade} `;
        }
    });

    $.ajax({
        url: 'http://localhost:5600/rest/api/v1/t2ss2t/synthesize',
        type: 'POST',
        data: JSON.stringify({
            'text': textToSpeech
        }),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        success: function (resp) {
            new Audio("data:audio/wav;base64," + resp.audio).play()
        }
    });

    return createAnswerElement(html);
}

/**
 *
 * @param value
 * @returns {HTMLDivElement}
 */
function handleStockIntent(value) {

    data = value.response['Time Series (Daily)'];

    stockTitle = value.response["Meta Data"]["2. Symbol"] + " " + value.response["Meta Data"]["3. Last Refreshed"]

    return createAnswerElement("", uuid);

}

function handleMapsIntent(value) {

    if (value.hasOwnProperty('response')) {

        mapData = value.response;

        return createAnswerElement("", uuid);

    }
}

let mapOptions, directionsService, directionsRenderer, stuttgart;

/**
 * Callback function for Google API
 */
function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    stuttgart = new google.maps.LatLng(48.77172146103744, 9.16245106247243);
    mapOptions = {
        zoom:7,
        center: stuttgart
    }

}

/**
 * Draws a Google map
 * @param uuid
 */
function drawMap(uuid) {
    let map = new google.maps.Map(document.getElementById(uuid), mapOptions);
    directionsRenderer.setMap(map);
}

/**
 * Calculates the requested route
 */
function calcRoute() {
    let temp = {
        "routes": mapData
    }

    function c() {
        var start = mapData[0]["legs"][0].start_address;
        var end = mapData[0]["legs"][0].end_address;
        var request = {
            origin: start,
            destination: end,
            travelMode: 'DRIVING'
        };
        directionsService.route(request, function(result, status) {
            if (status == 'OK') {
                directionsRenderer.setDirections(result);
            }
        });
    }

    c();
}


function handleDualisIntent(value) {

    if (value.hasOwnProperty('response')) {

        let response = value.response;

        // Check if array of exams got submitted
        if (response.constructor === Array) {

            response.forEach(module => {
                if (module.hasOwnProperty('name') && module.hasOwnProperty('exams')) {

                    let moduleName = module.name.split(" ")[0].trim();

                    grades[moduleName] = module.exams;
                    grades[moduleName].id = module.name;
                }
            })

            return createAnswerElement("Please select your module");

        }
    }

}

/**
 *
 * @param value
 * @returns {boolean|HTMLDivElement}
 */
function handleWeatherIntent(value) {

    // Check what weather intent got submitted
    if (value.hasOwnProperty('response')) {

        let response = value.response;

        // Check if it is a forecast request
        if (response.weather.constructor === Array) {

            let html = `<h1 class="dark:text-gray-300 font-light">Weather forecast for ${response.city_name}</h1>
                    <div class="h-0.5 dark:bg-gray-300 dark:bg-opacity-25 rounded my-1"></div>
                    <div class="flex">
                        ${handleMultipleWeatherData(response.weather)}
                    </div>`;

            return createAnswerElement(html);

        }

        // Check required weather fields
        if (response.hasOwnProperty('city_name') &&
            response.hasOwnProperty('time') &&
            response.hasOwnProperty('weather') &&
            response.hasOwnProperty('widget')) {

            let html = `<div>
                            <h1 class="dark:text-gray-300 font-light">Weather for ${response.city_name}</h1>
                            <div class="h-0.5 dark:bg-gray-300 dark:bg-opacity-25 rounded my-1"></div>
                            <div class="grid grid-rows-2 grid-cols-2">
                                <div class="h-32 flex justify-center items-center">
                                    <img class="h-24" src="http://openweathermap.org/img/wn/${response.weather.icon}@2x.png" alt="rain" id="weather-image">
                                </div>
                                <div class="h-32 flex justify-center items-center">
                                    <p class="dark:text-gray-100 font-normal text-7xl" id="temperature">${Math.round(response.weather.temp.current)}°C</p>
                                </div>
                                <div class="col-span-full flex flex-col pt-5 items-center">
                                    <p class="dark:text-gray-100 font-normal text-xl" id="weather-type">${response.weather.description}</p>
                                    <p class="dark:text-gray-500" id="wind-type">Wind: ${response.weather.wind.speed} m/s - Direction: ${response.weather.wind.deg}°</p>
                                    <p class="dark:text-gray-500" id="wind-type">Max Temp: ${response.weather.temp.max} - Min Temp: ${response.weather.temp.min} - Feels Like: ${response.weather.temp.feels_like}</p>
                                </div>
                            </div>
                        </div>`;

            return createAnswerElement(html);
        }

    }

    return false;

}

/**
 *
 * @param value
 */
function handleNewsIntent(value) {

    if (value.hasOwnProperty('response')) {

        let response = value.response;

        // Check if multiple data got returned
        if (response.constructor === Array) {

            let html = `${handleMultipleNewsData(response)}`;

            return createAnswerElement(html);

        }
    }
}

/**
 *
 * @param value
 * @returns {HTMLDivElement}
 */
function handleCalendarIntent(value) {

    if (value.hasOwnProperty('response')) {

        let response = value.response;

        if (response.constructor === Array) {

            let html = `${handleMultipleCalendarData(response)}`;

            return createAnswerElement(html);

        }
    }
}

/**
 *
 * @param value
 * @returns {boolean|HTMLDivElement}
 */
function handleSpotifyIntent(value) {

    if (value.hasOwnProperty('response')) {

        let response = value.response;

        // Check if multiple data got returned
        if (response.constructor === Array) {

            let html = `${handleMultipleSpotifyData(response)}`;

            return createAnswerElement(html);
        }

    }
    return false;
}

/**
 *
 * @param news
 * @returns {string}
 */
function handleMultipleNewsData(news) {

    let ret = "<div class='grid gap-y-2 h-56 overflow-auto'>";

    news.forEach(element => {

        if (element.hasOwnProperty('title') && element.hasOwnProperty('url') && element.hasOwnProperty('img')) {

            ret += `<a href="${element.url}" target="_blank"><div class="bg-gray-600 bg-opacity-30 h-28 rounded-xl p-3 flex items-center cursor-pointer">
                        <div class="w-40 mr-5">
                            <img class="rounded-md max-h-24 w-40" src="${element.img}" alt="news-image">
                        </div>
                        <div class="">
                            <p class="text-gray-300 text-xl">${element.title}</p>
                        </div>
                    </div></a>`;

        }

    })

    ret += "</div>";

    return ret;
}


/**
 *
 * @param appointments
 * @returns {string}
 */
function handleMultipleCalendarData(appointments) {

    let ret = "";

    appointments.forEach(element => {

        if (element.hasOwnProperty('htmlLink') && element.hasOwnProperty('summary') && element.hasOwnProperty('start') && element.hasOwnProperty('end')) {

            ret += `<a href="${element.htmlLink}" target="_blank">
                        <div class="dark:bg-black dark:bg-opacity-25 rounded-md h-20 p-2.5 shadow-2xl transition duration-500 ease-in-out transform-gpu hover:-translate-y-1 hover:scale-105 cursor-pointer">
                            <h1 class="dark:text-gray-300 font-light pb-1">${element.summary}</h1>
                            <p class="dark:text-green-500 font-thin">${new Date(Date.parse(element.start.dateTime)).getHours()}:${new Date(Date.parse(element.start.dateTime)).getMinutes()} - ${new Date(Date.parse(element.end.dateTime)).getHours()}:${new Date(Date.parse(element.end.dateTime)).getMinutes()} </p>
                        </div>
                    </a>`;
        }
    })

    return ret;
}

/**
 *
 * @param artists
 * @returns {string}
 */
function handleMultipleSpotifyData(artists) {

    let ret = "";

    if (artists.length % 2 === 0) {
        ret += `<div class="grid grid-rows-${(artists.length>10) ? 2 : 1} grid-cols-${artists.length/2} gap-2 m-6">`;
    } else {
        ret += `<div class="grid grid-rows-${(artists.length>10) ? 2 : 1} grid-cols-${artists.length/2 + 1} gap-2 m-6">`;
    }

    artists.forEach(element => {

        // If tracks got selected
        if (element.hasOwnProperty('artist') && element.hasOwnProperty('tracks') && element.hasOwnProperty('image') && element.hasOwnProperty('url')) {
            ret += `<a href="${element.url}" target="_blank">
                        <img class="h-36 w-36 rounded-md border shadow-2xl" src="${element.image}"/>
                        <p class="font-medium text-green-500">${element.artist}</p>
                        <p class="font-normal text-gray-500">${element.tracks}</p>    
                    </a>`;
        }
        else if(element.hasOwnProperty('name') && element.hasOwnProperty('image') && element.hasOwnProperty('url')) {
            ret += `<a href="${element.url}" target="_blank"><img class="h-36 w-36 rounded-md border shadow-2xl" src="${element.image}"/>
                    <p class="font-medium text-green-500">${element.name}</p></a>`;
        }
        else {
            ret += "";
        }

    })

    ret += "</div>";

    return ret;

}

/**
 *
 * @param message
 * @returns {*}
 */
function sendMessageToMiddleware(message) {
    return $.ajax({
        url: 'http://localhost:5600/rest/api/v1/dialogflow/query',
        type: 'POST',
        data: JSON.stringify({
            'message': message
        }),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader
    })
}

/**
 * createAnswerElement
 * @param {string} messagePayload
 * @param id
 * @returns {HTMLDivElement}
 */
function createAnswerElement(messagePayload, id = null) {

    // Create divs
    let div = document.createElement('div');
    let message = document.createElement('div');
    let header = document.createElement('div');

    div.classList.add("clearfix");
    message.classList.add('bg-gray-300', 'dark:bg-gray-900', 'dark:text-gray-300', 'left-0', 'float-left', 'mx-4', 'p-2', 'rounded-lg');
    header.classList.add('bg-gray-900', 'mx-6', 'rounded-t-xl', 'w-40', 'flex', 'justify-center', 'text-green-400', 'border-b', 'border-gray-800');

    header.innerText = "J.A.R.V.I.S at " + new Date().getHours() + ":" + new Date().getMinutes();

    if (id != null) {
        message.id = id;
        message.classList.add('w-2/3', 'h-96')
    }

    message.innerHTML = messagePayload;

    // Compose divs and return
    div.appendChild(header);
    div.appendChild(message);
    return div;
}

/**
 *
 * @param messagePayload
 * @returns {HTMLDivElement}
 */
function createChatElement(messagePayload) {
    // Create divs
    let div = document.createElement('div');
    let message = document.createElement('div');

    // Assign classes
    div.className = "clearfix";
    message.classList.add("bg-green-300");
    message.classList.add("mx-4");
    message.classList.add("my-2");
    message.classList.add("p-2");
    message.classList.add("rounded-lg");
    message.classList.add("right-0");
    message.classList.add("float-right");

    // Add message payload
    message.innerText = messagePayload;

    // Compose divs and return
    div.appendChild(message);
    return div;
}

function setHeader(xhr) {
    xhr.setRequestHeader('Access-Control-Allow-Headers', 'access-control-allow-methods, access-control-allow-origin');
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE');
}

/**
 * Generates a UUID
 * @returns {string}
 */
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
