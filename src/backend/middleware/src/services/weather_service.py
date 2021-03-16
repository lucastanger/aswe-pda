import requests


class WeatherService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://weather-service:5570/rest/api/v1'

    def query(self):
        response = self.current_weather()
        return

    def current_weather(self):
        if parameters['unit']:
            # use parameter['unit'] as unit
            pass
        else:
            # load unit from config
            pass

        if parameters['city'] and not (parameters['lat'] or parameters['lon']):
            # make request with city and unit
            pass
        elif parameters['lat'] and parameters['lon'] and not parameters['city']:
            # make request with lat and lon and unit
            pass
        else:
            # load city from config
            pass

        pass

    def forecast(self):
        if parameters['unit']:
            # use parameter['unit'] as unit
            pass
        else:
            # load unit from config
            pass

        if parameters['days']:
            # use days from parameters
            pass

        if parameters['city'] and not (parameters['lat'] or parameters['lon']):
            # make request with city and unit
            pass
        elif parameters['lat'] and parameters['lon'] and not parameters['city']:
            # make request with lat and lon and unit
            pass
        else:
            # load city from config
            pass

        pass
