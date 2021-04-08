# Import setup and teardown.
from tests.BaseCase import BaseCase

from unittest import mock
import requests


class SymbolTest(BaseCase):
    @mock.patch("requests.get")
    def test_get_symbol_success(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            "bestMatches": [
                {
                    "1. symbol": "TL0.DEX",
                    "2. name": "Tesla",
                    "3. type": "Equity",
                    "4. region": "XETRA",
                    "5. marketOpen": "08:00",
                    "6. marketClose": "20:00",
                    "7. timezone": "UTC+02",
                    "8. currency": "EUR",
                    "9. matchScore": "1.0000",
                },
                {
                    "1. symbol": "TL0.FRK",
                    "2. name": "Tesla",
                    "3. type": "Equity",
                    "4. region": "Frankfurt",
                    "5. marketOpen": "08:00",
                    "6. marketClose": "20:00",
                    "7. timezone": "UTC+02",
                    "8. currency": "EUR",
                    "9. matchScore": "1.0000",
                },
                {
                    "1. symbol": "TSLA34.SAO",
                    "2. name": "Tesla",
                    "3. type": "Equity",
                    "4. region": "Brazil/Sao Paolo",
                    "5. marketOpen": "10:00",
                    "6. marketClose": "17:30",
                    "7. timezone": "UTC-03",
                    "8. currency": "BRL",
                    "9. matchScore": "1.0000",
                },
                {
                    "1. symbol": "TSLA",
                    "2. name": "Tesla Inc",
                    "3. type": "Equity",
                    "4. region": "United States",
                    "5. marketOpen": "09:30",
                    "6. marketClose": "16:00",
                    "7. timezone": "UTC-04",
                    "8. currency": "USD",
                    "9. matchScore": "0.8889",
                },
                {
                    "1. symbol": "TXLZF",
                    "2. name": "Tesla Exploration Ltd",
                    "3. type": "Equity",
                    "4. region": "United States",
                    "5. marketOpen": "09:30",
                    "6. marketClose": "16:00",
                    "7. timezone": "UTC-04",
                    "8. currency": "USD",
                    "9. matchScore": "0.4000",
                },
            ]
        }

        keyword = "tesla"
        code = 200
        symbol = "TL0.DEX"

        # Act
        response = self.app.get("/rest/api/v1/symbol?keyword={}".format(keyword))

        # Assert
        self.assertEqual(response.json["bestMatches"][0]["1. symbol"], symbol)
        self.assertEqual(response.status_code, code)

    @mock.patch("requests.get")
    def test_get_symbol_api_failure(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            "Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency."
        }

        keyword = "tesla"
        code = 500
        info = "Internal server error caused by third party api."

        # Act
        response = self.app.get("/rest/api/v1/symbol?keyword={}".format(keyword))

        # Assert
        self.assertEqual(response.json["info"], info)
        self.assertEqual(response.status_code, code)

    @mock.patch("requests.get")
    def test_get_symbol_no__keyword_failure(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY."
        }

        keyword = ""
        code = 500
        info = "Internal server error caused by third party api."

        # Act
        response = self.app.get("/rest/api/v1/symbol?keyword={}".format(keyword))

        # Assert
        self.assertEqual(response.json["info"], info)
        self.assertEqual(response.status_code, code)

    @mock.patch("requests.get")
    def test_get_symbol_wrong__keyword_failure(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {"bestMatches": []}

        keyword = "sesesesese"
        code = 400
        error = "No matches found."

        # Act
        response = self.app.get("/rest/api/v1/symbol?keyword={}".format(keyword))

        # Assert
        self.assertEqual(response.json["error"], error)
        self.assertEqual(response.status_code, code)
