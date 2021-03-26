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

            for (let i = 0; i<4; i++) {

                calendar.innerHTML += createCalendarElement(response.response[i]);

            }


        },
        error: function (error) {
            console.log(error)
        },
        complete: stopLoader('calendarloader')

    })

}

function createCalendarElement(event) {

    return `<a href="" target="_blank"><div class="dark:bg-black dark:bg-opacity-25 rounded-md h-20 p-2.5 shadow-2xl transition duration-500 ease-in-out transform-gpu hover:-translate-y-1 hover:scale-105 cursor-pointer">
                            <h1 class="dark:text-gray-300 font-light pb-1">Meeting "Online Learning" Team</h1>
                            <p class="dark:text-green-500 font-thin">14:00 - 16:00</p>
                        </div></a>`;



}

