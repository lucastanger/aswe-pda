# Import setup and teardown.
from tests.BaseCase import BaseCase


class CurrentWeatherTest(BaseCase):
    def test_successful_current_weather_get(self):
        # Arrange
        city = 'Stuttgart'
        unit = 'metric'

        # Act
        response = self.app.get(
            '/rest/api/v1/current-weather?city={}&unit={}'.format(city, unit)
        )

        # Assert
        self.assertEqual(response.json['city_name'], city)
        self.assertIs(type(response.json['weather']['temp']['current']), float)
        self.assertEqual(response.status_code, 200)

    def test_failure_current_weather_get(self):
        # Arrange
        city = ''
        error = 'Either `city` or `lat` and `lon` are required.'
        code = 400
        unit = 'metric'

        # Act
        response = self.app.get(
            '/rest/api/v1/current-weather?city={}&unit={}'.format(city, unit)
        )

        # Assert
        self.assertEqual(response.json['error'], error)
        self.assertEqual(response.status_code, code)
