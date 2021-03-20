import requests
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(host='mongo', port=27017)
db = client['aswe-pda']
db.authenticate('dev', 'dev')
configuration = db['configuration']


class WeatherService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://weather-service:5570/rest/api/v1'

    def query(self):
        print(self.parameters)
        # load config
        config = configuration.find_one(
            {
                'general': {'$exists': True},
                'dualisService': {'$exists': True},
                'newsService': {'$exists': True},
                'weatherService': {'$exists': True},
                'stocksService': {'$exists': True},
            }
        )
        del config['_id']

        lat = config['weatherService']['location']['lat']
        lon = config['weatherService']['location']['lon']
        unit = config['weatherService']['unit']

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
