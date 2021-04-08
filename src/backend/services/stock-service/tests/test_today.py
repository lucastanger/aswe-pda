# Import setup and teardown.
from tests.BaseCase import BaseCase

from unittest import mock
import requests


class TodayTest(BaseCase):
    @mock.patch("requests.get")
    def test_get_today_success(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            "Global Quote": {
                "01. symbol": "TSLA",
                "02. open": "687.0000",
                "03. high": "691.3800",
                "04. low": "667.8400",
                "05. price": "670.9700",
                "06. volume": "26309433",
                "07. latest trading day": "2021-04-07",
                "08. previous close": "691.6200",
                "09. change": "-20.6500",
                "10. change percent": "-2.9857%",
            }
        }

        symbol = "TSLA"
        code = 200

        # Act
        response = self.app.get("/rest/api/v1/today?symbol={}".format(symbol))

        # Assert
        self.assertEqual(response.json["symbol"]["01. symbol"], symbol)
        self.assertEqual(response.status_code, code)

    @mock.patch("requests.get")
    def test_get_today_api_failure(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            "Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency."
        }

        symbol = "TSLA"
        info = "Internal server error caused by third party api."
        code = 500

        # Act
        response = self.app.get("/rest/api/v1/today?symbol={}".format(symbol))

        # Assert
        self.assertEqual(response.json["info"], info)
        self.assertEqual(response.status_code, code)

    @mock.patch("requests.get")
    def test_get_today_no_symbol_failure(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for GLOBAL_QUOTE."
        }

        symbol = ""
        code = 400
        error = "No symbol found."

        # Act
        response = self.app.get("/rest/api/v1/today?symbol={}".format(symbol))

        # Assert
        self.assertEqual(response.json["error"], error)
        self.assertEqual(response.status_code, code)

    @mock.patch("requests.get")
    def test_get_today_wrong_symbol_failure(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {"Global Quote": {}}

        symbol = "asasasasas"
        code = 400
        error = "No symbol found."

        # Act
        response = self.app.get("/rest/api/v1/today?symbol={}".format(symbol))

        # Assert
        self.assertEqual(response.json["error"], error)
        self.assertEqual(response.status_code, code)
