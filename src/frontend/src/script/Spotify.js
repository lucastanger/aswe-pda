// Spotify
const recentArtists = document.getElementById('recent-artists');

$(document).ready(function () {

    sendMessageToMiddleware('Profile artist').then(function (res) {
        console.log(res)

        let html = "";

        res.response = res.response.slice(0, 5);

        res.response.forEach(entry => {

            html += `<div class="items-center w-40 flex flex-col transition duration-500 ease-in-out transform-gpu hover:-translate-y-1 hover:scale-110 cursor-pointer">
                            <a href="${entry.url}" target="_blank">
                                <div class="bg-gray-400 mb-2 h-40 w-40 rounded-md border shadow-2xl overflow-auto">
                                    <img class="rounded-md" src="${entry.image}" alt="${entry.name}" width="158" height="158">
                                </div>
                                <p class="font-medium text-green-500">${entry.name}</p>
                            </a>
                        </div>`;

        });

        recentArtists.innerHTML = html;
    });
});

function sendMessageToMiddleware(message) {

    return $.ajax({
        url: 'http://localhost:5600/rest/api/v1/dialogflow/query',
        type: 'POST',
        data: JSON.stringify({
            'message': message
        }),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        complete: stopLoader()
    });
}

function stopLoader() {
    document.getElementById('artistsloader').remove()
}

function setHeader(xhr) {
    xhr.setRequestHeader('Access-Control-Allow-Headers', 'access-control-allow-methods, access-control-allow-origin');
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE');
}
