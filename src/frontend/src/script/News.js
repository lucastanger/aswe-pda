// News.js
const newsContainer = document.getElementById('newsContainer');

// If document is ready, start news query
$(document).ready(function () {

    retrieveNewsForTheDay();

});

function retrieveNewsForTheDay() {

    $.ajax({
        url: 'http://localhost:5600/rest/api/v1/dialogflow/query',
        type: 'POST',
        data: JSON.stringify({
            'message': 'Top'
        }),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        success: function (response) {

            for (let i = 0; i<4; i++) {

                newsContainer.innerHTML += createNewsElement(response.response[i]);
            }

        },
        error: function (error) {
            console.log(error)
        },
        complete: stopLoader('newsloader')
    })
}



function createNewsElement(news) {

    return `<a href="${news.url}" target="_blank"><div class="bg-gray-600 bg-opacity-30 h-28 rounded-xl p-3 flex items-center transition duration-500 ease-in-out transform-gpu hover:-translate-y-1 hover:scale-105 cursor-pointer">
                            <!-- news image -->
                            <div class="w-40 mr-5">
                                <img class="rounded-md max-h-24 w-40" src="${news.img}" alt="">
                            </div>
                            <!-- end news image -->
                            <!-- news text -->
                            <div class="">
                                <p class="text-gray-300 text-xl">${news.title}</p>
                            </div>
                            <!-- end news text -->
                        </div></a>`;

}
