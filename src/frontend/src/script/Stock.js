// Stock.js
const stockContainer = document.getElementById('stockContainer')

$(document).ready(function () {

    retrieveStocks();

})

function retrieveStocks() {

    $.ajax({
        url: 'http://localhost:5600/rest/api/v1/dialogflow/query',
        type: 'POST',
        data: JSON.stringify({
            'message': 'stocks'
        }),
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        success: function (response) {

            // If response is not empty
            if (response) {
                let data = response.response['Time Series (Daily)'];

                createStockPlot(data, 'stockContainer', response.response["Meta Data"]["2. Symbol"] + " " + response.response["Meta Data"]["3. Last Refreshed"]);
            }

        },
        error: function (error) {
            console.log(error)
        }
    })
}

/**
 *
 * @param data
 * @param where
 * @param title
 */
function createStockPlot(data, where, title = null) {

    let trace = [
        createTrace('High', data, '2. high', '#F54E2A'),
        createTrace('Low', data, '3. low', '#2A6EF5')
    ];

    let layout = {
        title: title,
    };

    var config = {responsive: true}

    Plotly.newPlot(where, trace, layout, config);
}

/**
 * Create plottable time series trace
 * @param name
 * @param data
 * @param color
 * @returns {{mode: string, line: {color: string}, name, x: string[], y: [], type: string}}
 */
function createTrace(name, data, col, color = '#17BECF') {

    return trace = {
        type: 'scatter',
        mode: 'lines',
        name: name,
        x: Object.keys(data),
        y: unpack(data, col),
        line: {color: color}
    }

    /**
     * Unpack trace data
     * @param data
     * @param col
     * @returns {[]}
     */
    function unpack(data, col) {

        let ret = [];

        Object.keys(data).forEach(k => {
            ret.push(data[k][col]);
        })

        return ret;
    }
}
