// Calendar.js
const calendar = document.getElementById('calendarContainer');

$(document).ready(function () {

    retrieveAppointmentsForTheDay();

});

// Get information about appointments for the day
function retrieveAppointmentsForTheDay() {

    $.ajax({
        url: 'http://localhost:5600/rest/api/v1/dialogflow/query',
        type: 'POST',
        data: JSON.stringify({
            'message': "agenda today"
        }),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        success: function (response) {

            if (response.response.constructor === Array) {
                response.response.forEach(event => {

                    calendar.innerHTML += createCalendarElement(event);

                })
            }

            stopLoader('calendarloader')

        },
        error: function (error) {
            console.log(error)
        }

    })

}

/**
 *
 * @param event
 * @returns {string}
 */
function createCalendarElement(event) {

    if (event.hasOwnProperty('htmlLink') && event.hasOwnProperty('summary') && event.hasOwnProperty('start') && event.hasOwnProperty('end')) {
        return `<a href="${event.htmlLink}" target="_blank">
                <div class="dark:bg-black dark:bg-opacity-25 rounded-md h-20 p-2.5 shadow-2xl transition duration-500 ease-in-out transform-gpu hover:-translate-y-1 hover:scale-105 cursor-pointer">
                    <h1 class="dark:text-gray-300 font-light pb-1">${event.summary}</h1>
                    <p class="dark:text-green-500 font-thin">${new Date(Date.parse(event.start.dateTime)).getHours()}:${new Date(Date.parse(event.start.dateTime)).getMinutes()} - ${new Date(Date.parse(event.end.dateTime)).getHours()}:${new Date(Date.parse(event.end.dateTime)).getMinutes()} </p>
                </div>
            </a>`;
    } else {
        return `<div class="dark:bg-black dark:bg-opacity-25 rounded-md h-20 p-2.5 shadow-2xl transition duration-500 ease-in-out transform-gpu hover:-translate-y-1 hover:scale-105 cursor-pointer">
                    <h1 class="dark:text-gray-300 font-light pb-1">${event.summary}</h1>
                    <p class="dark:text-green-500 font-thin">${event.start.dateTime} - ${event.end.dateTime}</p>
                </div>`;
    }





}

