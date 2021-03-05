/**
 * Class HttpRequest
 * Creates a http request.
 * @param body Defines the payload for the request
 * @package requests
 */
class HttpRequest {
    constructor(body)
    {
        this.body = body;
    }

    /**
     * Send the http request
     * @returns {Promise<Array>} Message and data of the result
     */
    send()
    {
        return new Promise((resolve, reject) => $.ajax({
            url: 'https://jsonplaceholder.typicode.com/todos/1',
            accepts: {json: 'application/json'},
            dataType: 'json',
            method: 'GET',
            data: this.body,
            success: (result) => {
                // Get message with: result.message
                // Get data with: result.data
                resolve(result);
            },
            error: (result) => {
                // Get message with: result.responseJSON.message
                // Get data with: result.responseJSON.data
                reject(result);
            }
        }));
    }
}

$(document).ready(function() {
    const request = new HttpRequest({test: 'test'});
    request.send().then(result => {
        console.log(result);
    }).catch(result => {
        console.log(result);
    });

});
