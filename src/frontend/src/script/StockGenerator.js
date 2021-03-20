const stockInput = document.getElementById('stock');

const tmp = '{\n' +
    '    "bestMatches": [\n' +
    '        {\n' +
    '            "1. symbol": "A",\n' +
    '            "2. name": "Agilent Technologies Inc",\n' +
    '            "3. type": "Equity",\n' +
    '            "4. region": "United States",\n' +
    '            "5. marketOpen": "09:30",\n' +
    '            "6. marketClose": "16:00",\n' +
    '            "7. timezone": "UTC-04",\n' +
    '            "8. currency": "USD",\n' +
    '            "9. matchScore": "1.0000"\n' +
    '        },\n' +
    '        {\n' +
    '            "1. symbol": "A.TRV",\n' +
    '            "2. name": "Armor Minerals Inc",\n' +
    '            "3. type": "Equity",\n' +
    '            "4. region": "Toronto Venture",\n' +
    '            "5. marketOpen": "09:30",\n' +
    '            "6. marketClose": "16:00",\n' +
    '            "7. timezone": "UTC-05",\n' +
    '            "8. currency": "CAD",\n' +
    '            "9. matchScore": "0.5000"\n' +
    '        },\n' +
    '        {\n' +
    '            "1. symbol": "A0I.FRK",\n' +
    '            "2. name": "A0I",\n' +
    '            "3. type": "Equity",\n' +
    '            "4. region": "Frankfurt",\n' +
    '            "5. marketOpen": "08:00",\n' +
    '            "6. marketClose": "20:00",\n' +
    '            "7. timezone": "UTC+02",\n' +
    '            "8. currency": "EUR",\n' +
    '            "9. matchScore": "0.5000"\n' +
    '        },\n' +
    '        {\n' +
    '            "1. symbol": "A02.FRK",\n' +
    '            "2. name": "Adways Inc",\n' +
    '            "3. type": "Equity",\n' +
    '            "4. region": "Frankfurt",\n' +
    '            "5. marketOpen": "08:00",\n' +
    '            "6. marketClose": "20:00",\n' +
    '            "7. timezone": "UTC+02",\n' +
    '            "8. currency": "EUR",\n' +
    '            "9. matchScore": "0.3333"\n' +
    '        },\n' +
    '        {\n' +
    '            "1. symbol": "A04.FRK",\n' +
    '            "2. name": "Ascential plc",\n' +
    '            "3. type": "Equity",\n' +
    '            "4. region": "Frankfurt",\n' +
    '            "5. marketOpen": "08:00",\n' +
    '            "6. marketClose": "20:00",\n' +
    '            "7. timezone": "UTC+02",\n' +
    '            "8. currency": "EUR",\n' +
    '            "9. matchScore": "0.3333"\n' +
    '        },\n' +
    '        {\n' +
    '            "1. symbol": "A08.FRK",\n' +
    '            "2. name": "At Home Group Inc",\n' +
    '            "3. type": "Equity",\n' +
    '            "4. region": "Frankfurt",\n' +
    '            "5. marketOpen": "08:00",\n' +
    '            "6. marketClose": "20:00",\n' +
    '            "7. timezone": "UTC+02",\n' +
    '            "8. currency": "EUR",\n' +
    '            "9. matchScore": "0.3333"\n' +
    '        },\n' +
    '        {\n' +
    '            "1. symbol": "A0T.FRK",\n' +
    '            "2. name": "American Tower Corporation (REIT)",\n' +
    '            "3. type": "Equity",\n' +
    '            "4. region": "Frankfurt",\n' +
    '            "5. marketOpen": "08:00",\n' +
    '            "6. marketClose": "20:00",\n' +
    '            "7. timezone": "UTC+02",\n' +
    '            "8. currency": "EUR",\n' +
    '            "9. matchScore": "0.3333"\n' +
    '        },\n' +
    '        {\n' +
    '            "1. symbol": "A0W.FRK",\n' +
    '            "2. name": "Arrow Global Group PLC",\n' +
    '            "3. type": "Equity",\n' +
    '            "4. region": "Frankfurt",\n' +
    '            "5. marketOpen": "08:00",\n' +
    '            "6. marketClose": "20:00",\n' +
    '            "7. timezone": "UTC+02",\n' +
    '            "8. currency": "EUR",\n' +
    '            "9. matchScore": "0.3333"\n' +
    '        },\n' +
    '        {\n' +
    '            "1. symbol": "A16.FRK",\n' +
    '            "2. name": "ASR Nederland N.V",\n' +
    '            "3. type": "Equity",\n' +
    '            "4. region": "Frankfurt",\n' +
    '            "5. marketOpen": "08:00",\n' +
    '            "6. marketClose": "20:00",\n' +
    '            "7. timezone": "UTC+02",\n' +
    '            "8. currency": "EUR",\n' +
    '            "9. matchScore": "0.3333"\n' +
    '        },\n' +
    '        {\n' +
    '            "1. symbol": "A0U2.FRK",\n' +
    '            "2. name": "Azincourt Energy Corp",\n' +
    '            "3. type": "Equity",\n' +
    '            "4. region": "Frankfurt",\n' +
    '            "5. marketOpen": "08:00",\n' +
    '            "6. marketClose": "20:00",\n' +
    '            "7. timezone": "UTC+02",\n' +
    '            "8. currency": "EUR",\n' +
    '            "9. matchScore": "0.2857"\n' +
    '        }\n' +
    '    ]\n' +
    '}'

// Enter Press Event Listener
stockInput.addEventListener('keypress', function (key) {
    console.log(key);

    if (key.code === 'Enter') {
        requestStockList(stockInput.value)
    }
});

function requestStockList(searchIndex) {

    $.ajax({
        url: `http://localhost:5585/rest/api/v1/symbol?keyword=${searchIndex}`,
        type: 'GET',
        crossDomain: true,
        beforeSend: setHeader,
        success: createStockTiles(tmp),
        error: function (error) {
            console.log(error)
        }
    })
}

function setHeader(xhr) {
    xhr.setRequestHeader('Access-Control-Allow-Headers', 'access-control-allow-methods, access-control-allow-origin');
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE');
}

function createStockTiles(stocks) {

    let stock = JSON.parse(stocks)["bestMatches"]

    let stockContainer = document.getElementById('stockContainer');

    for (let element of stock) {

        let stockElement = document.createElement('div');
        let innerStockElement = document.createElement('div');
        let desc = document.createElement('p');

        stockElement.classList.add('flex', 'flex-row', 'items-center');
        innerStockElement.classList.add('rounded', 'border', 'border-gray-300', 'h-20', 'w-20', 'flex', 'items-center', 'justify-center', 'mr-8', 'bg-gray-50', 'bg-opacity-20');
        desc.classList.add('uppercase');

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
