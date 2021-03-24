// Spotify
const spotifyButton = document.getElementById('spotify-button');


$(document).ready(function () {
    // Add onClick Event
    spotifyButton.addEventListener('click', function () {

        $.ajax({
            url: 'http://localhost:5600/rest/api/v1/authorization/spotify-service',
            type: 'GET',
            crossDomain: true,
            contentType: 'application/json',
            beforeSend: setHeader,
            success: function (response) {
                if (response['authorization_url']) {
                    window.open(response['authorization_url'], '_blank').focus()
                } else {
                    alert('Looks like there is no valid response!')
                }
            },
            error: function (error) {
                console.log('Could not reach the middleware! Error:')
                console.log(error)
            }

        });

    })
});

function setHeader(xhr) {
    xhr.setRequestHeader('Access-Control-Allow-Headers', 'access-control-allow-methods, access-control-allow-origin');
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE');
}
