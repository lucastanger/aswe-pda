# Imports.
import unittest
import json

# Import setup and teardown.
from tests.BaseCase import BaseCase


class CurrentWeatherTest(BaseCase):
    def test_successful_current_weather_get(self):
        # Arrange
        city = "Stuttgart"

        # Act
        response = self.app.get("/rest/api/v1/current-weather?city={}".format(city))

        # Assert
        self.assertEqual(response.json["city_name"], city)
        self.assertIs(type(response.json["weather"]["temp"]["current"]), float)
        self.assertEqual(response.status_code, 200)

    def test_failure_current_weather_get(self):
        # Arrange
        city = ""
        info = "Internal server error caused by third party api."
        code = 400

        # Act
        response = self.app.get("/rest/api/v1/current-weather?city={}".format(city))

        # Assert
        self.assertEqual(response.json["info"], info)
        self.assertEqual(response.json["error"]["code"], code)
        self.assertEqual(response.status_code, 500)
