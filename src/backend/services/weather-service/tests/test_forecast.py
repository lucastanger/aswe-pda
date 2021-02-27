# Import setup and teardown.
from tests.BaseCase import BaseCase


class ForecastTest(BaseCase):
    def test_successful_forecast_get(self):
        # Arrange
        city = 'Stuttgart'

        # Act
        response = self.app.get('/rest/api/v1/forecast?city={}'.format(city))

        # Assert
        self.assertEqual(response.json['city_name'], city)
        self.assertEqual(len(response.json['weather']), 8)
        self.assertIs(type(response.json['weather'][0]['temp']['day']), float)
        self.assertEqual(response.status_code, 200)

    def test_failure_forecast_get(self):
        # Arrange
        city = ''
        info = 'Internal server error caused by third party api.'
        code = 400

        # Act
        response = self.app.get('/rest/api/v1/forecast?city={}'.format(city))

        # Assert
        self.assertEqual(response.json['info'], info)
        self.assertEqual(response.json['error']['code'], code)
        self.assertEqual(response.status_code, 500)
