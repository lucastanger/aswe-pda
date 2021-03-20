const stockInput = document.getElementById('stock');

// Enter Press Event Listener
stockInput.addEventListener('keypress', function (key) {
    if (key.code === 'Enter') {
        requestStockList(stockInput.value)
    }
});

function requestStockList(searchIndex) {

    $.ajax({
        url: `http://localhost:5600/rest/api/v1/configuration/stock-service/symbol?keyword=${searchIndex}`,
        type: 'GET',
        crossDomain: true,
        contentType: 'application/json',
        beforeSend: setHeader,
        success: createStockTiles,
        error: function (error) {
            console.log(error)
        }
    })
}

function setSelected(stock) {
    document.getElementById('selectedStock').innerText = stock;
}

function setHeader(xhr) {
    xhr.setRequestHeader('Access-Control-Allow-Headers', 'access-control-allow-methods, access-control-allow-origin');
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE');
}

function createStockTiles(stocks) {

    //let stock = JSON.parse(stocks)["bestMatches"]

    let stockContainer = document.getElementById('stockContainer');

    // Clear previous results
    stockContainer.innerText = "";

    for (let element of stocks['bestMatches']) {

        let stockElement = document.createElement('div');
        let innerStockElement = document.createElement('div');
        let desc = document.createElement('p');

        stockElement.classList.add('flex', 'flex-row', 'items-center');
        innerStockElement.classList.add('rounded', 'border', 'border-gray-300', 'h-20', 'w-20', 'flex', 'items-center', 'justify-center', 'mr-8', 'bg-gray-50', 'bg-opacity-20', 'cursor-pointer');
        innerStockElement.id = element['2. name'];
        desc.classList.add('uppercase');

        stockElement.addEventListener('click', function () {

            setSelected(this.firstChild.innerText);

        });

        innerStockElement.innerText = element['1. symbol'];
        desc.innerText = element['2. name'];

        stockElement.append(innerStockElement, desc);

        stockContainer.append(stockElement);
    }
}

class StockGenerator {

    constructor() {



    }


}
