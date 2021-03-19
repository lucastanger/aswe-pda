# Import setup and teardown.
from tests.BaseCase import BaseCase


class ForecastTest(BaseCase):
    def test_successful_forecast_get(self):
        # Arrange
        city = 'Stuttgart'
        unit = 'metric'

        # Act
        response = self.app.get(
            '/rest/api/v1/forecast?city={}&unit={}'.format(city, unit)
        )

        # Assert
        self.assertEqual(response.json['city_name'], city)
        self.assertEqual(len(response.json['weather']), 8)
        self.assertIs(type(response.json['weather'][0]['temp']['day']), float)
        self.assertEqual(response.status_code, 200)

    def test_failure_forecast_get(self):
        # Arrange
        city = ''
        error = 'Either `city` or `lat` and `lon` are required.'
        code = 400
        unit = 'metric'

        # Act
        response = self.app.get(
            '/rest/api/v1/forecast?city={}&unit={}'.format(city, unit)
        )

        # Assert
        self.assertEqual(response.json['error'], error)
        self.assertEqual(response.status_code, code)
