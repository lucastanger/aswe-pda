// NewsGenerator.js
const newsSelect = document.getElementById('newspaper');

$(document).ready(function () {

    $.ajax({
        url: `http://localhost:5600/rest/api/v1/dialogflow/query`,
        type: 'POST',
        data: JSON.stringify({
            'message': 'Sources'
        }),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        success: function (response) {

            if (response.hasOwnProperty('response')) {

                response.response.forEach(element => {
                    let option = document.createElement('option');
                    option.innerText = element.name;
                    newsSelect.appendChild(option);

                });

            }
        },
        error: function (error) {
            console.log(error)
        }
    })

})
