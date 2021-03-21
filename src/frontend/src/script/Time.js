// Time generator class
const timeDisplay = document.getElementById('time');
const dateDisplay = document.getElementById('date');

$(document).ready(function() {
    // Initial execution of function
    displayTime(timeDisplay);
    displayDate(dateDisplay);
    setInterval(function() {
        displayTime(timeDisplay);
    }, 1000);
});

// Implement Observer??

function displayTime(dom) {

    let today = new Date();
    let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getUTCSeconds();

    dom.innerText = time;
}

function displayDate(dom) {

    let today = new Date();
    let date = today.toLocaleDateString('en', { weekday: 'long' }) + ", " + today.toLocaleString('en', { month: 'long' }) + " " + today.getDate() + ", " + today.getFullYear();

    dom.innerText = date;
}


