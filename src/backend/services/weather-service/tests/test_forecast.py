# Import setup and teardown.
from tests.BaseCase import BaseCase

from unittest import mock
import requests


class ForecastTest(BaseCase):
    @mock.patch("requests.get")
    def test_get_forecast_city_success(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            "city": {
                "id": 2825297,
                "name": "Stuttgart",
                "coord": {"lon": 9.177, "lat": 48.7823},
                "country": "DE",
                "population": 589793,
                "timezone": 7200,
            },
            "cod": "200",
            "message": 0.1233915,
            "cnt": 1,
            "list": [
                {
                    "dt": 1617706800,
                    "sunrise": 1617684622,
                    "sunset": 1617732035,
                    "temp": {
                        "day": 3.83,
                        "min": -2.14,
                        "max": 4.74,
                        "night": 0.89,
                        "eve": 2.92,
                        "morn": -1.82,
                    },
                    "feels_like": {
                        "day": -0.55,
                        "night": -6.64,
                        "eve": -1.03,
                        "morn": -6.64,
                    },
                    "pressure": 1014,
                    "humidity": 58,
                    "weather": [
                        {
                            "id": 600,
                            "main": "Snow",
                            "description": "light snow",
                            "icon": "13d",
                        }
                    ],
                    "speed": 5.92,
                    "deg": 285,
                    "clouds": 97,
                    "pop": 0.99,
                    "snow": 2.67,
                }
            ],
        }

        city = "Stuttgart"
        unit = "metric"
        days = "1"

        # Act
        response = self.app.get(
            "/rest/api/v1/forecast?city={}&days={}&unit={}".format(city, days, unit)
        )

        # Assert
        self.assertEqual(response.json["city_name"], city)
        self.assertIs(type(response.json["weather"][0]["icon"]), str)
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.get")
    def test_get_forecast_lat_lon_success(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            "city": {
                "id": 2825297,
                "name": "Stuttgart",
                "coord": {"lon": 9.1833, "lat": 48.7833},
                "country": "DE",
                "population": 589793,
                "timezone": 7200,
            },
            "cod": "200",
            "message": 5.0614238,
            "cnt": 1,
            "list": [
                {
                    "dt": 1617706800,
                    "sunrise": 1617684620,
                    "sunset": 1617732034,
                    "temp": {
                        "day": 3.88,
                        "min": -2.05,
                        "max": 4.8,
                        "night": 0.96,
                        "eve": 2.89,
                        "morn": -1.74,
                    },
                    "feels_like": {
                        "day": -0.49,
                        "night": -6.55,
                        "eve": -1.06,
                        "morn": -6.55,
                    },
                    "pressure": 1014,
                    "humidity": 58,
                    "weather": [
                        {
                            "id": 600,
                            "main": "Snow",
                            "description": "light snow",
                            "icon": "13d",
                        }
                    ],
                    "speed": 5.91,
                    "deg": 285,
                    "clouds": 97,
                    "pop": 0.99,
                    "snow": 2.71,
                }
            ],
        }

        lat = 48.783333
        lon = 9.183333
        city = "Stuttgart"
        unit = "metric"
        days = "1"

        # Act
        response = self.app.get(
            "/rest/api/v1/forecast?lat={}&lon={}&days={}&unit={}".format(
                lat, lon, days, unit
            )
        )

        # Assert
        self.assertEqual(response.json["city_name"], city)
        self.assertEqual(len(response.json["weather"]), 1)
        self.assertIs(type(response.json["weather"][0]["icon"]), str)
        self.assertEqual(response.status_code, 200)

    def test_get_forecast_no_city_failure(self):
        # Arrange
        city = ""
        error = "Either `city` or `lat` and `lon` are required."
        code = 400
        unit = "metric"

        # Act
        response = self.app.get(
            "/rest/api/v1/forecast?city={}&unit={}".format(city, unit)
        )

        # Assert
        self.assertEqual(response.json["error"], error)
        self.assertEqual(response.status_code, code)

    @mock.patch("requests.get")
    def test_get_forecast_wrong_response_failure(self, mock_request):
        # Arrange
        mock_resp = requests.models.Response()
        mock_resp.status_code = 404
        mock_resp.json = {"message": "Internal error"}
        mock_request.return_value = mock_resp
        city = "Stuttgart"
        unit = "metric"
        info = "Internal server error caused by third party api."
        code = 500

        # Act
        response = self.app.get(
            "/rest/api/v1/forecast?city={}&unit={}".format(city, unit)
        )

        # Assert
        self.assertEqual(response.status_code, code)