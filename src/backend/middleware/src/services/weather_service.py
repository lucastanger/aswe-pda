from datetime import datetime

import requests
from src.util.mongodb import MongoDB


class WeatherService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://weather-service:5570/rest/api/v1'

    def query(self):
        print(self.parameters)
        # load config
        config = MongoDB.instance().db['configuration'].find_one({'weather': {'$exists': True},})

        lat = config['weather']['_location']['_lat']
        lon = config['weather']['_location']['_lon']
        unit = config['weather']['_unit']

        if self.parameters['date-period']:
            startDate = datetime.strptime(
                self.parameters['date-period']['startDate'], '%Y-%m-%dT%H:%M:%S%z'
            )
            endDate = datetime.strptime(
                self.parameters['date-period']['endDate'], '%Y-%m-%dT%H:%M:%S%z'
            )
            delta = endDate - startDate
            days = delta.days + 1

            response = self.get_forecast(self.parameters['city'], lat, lon, days, unit)
        else:
            response = self.get_current_weather(self.parameters['city'], lat, lon, unit)

        return response.json()

    def get_forecast(self, city, lat, lon, days, unit):
        if days:
            if city:
                response = requests.get(
                    f'{self.base_url}/forecast',
                    params={'city': city, 'days': days, 'unit': unit},
                )
            else:
                response = requests.get(
                    f'{self.base_url}/forecast',
                    params={'lat': lat, 'lon': lon, 'days': days, 'unit': unit},
                )
        else:
            if city:
                response = requests.get(
                    f'{self.base_url}/forecast', params={'city': city, 'unit': unit}
                )
            else:
                response = requests.get(
                    f'{self.base_url}/forecast',
                    params={'lat': lat, 'lon': lon, 'unit': unit},
                )

        return response

    def get_current_weather(self, city, lat, lon, unit):
        if city:
            response = requests.get(
                f'{self.base_url}/current-weather', params={'city': city, 'unit': unit}
            )
        else:
            response = requests.get(
                f'{self.base_url}/current-weather',
                params={'lat': lat, 'lon': lon, 'unit': unit},
            )

        return response
