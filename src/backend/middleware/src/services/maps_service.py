import requests


class MapsService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://maps-service:5580/rest/api/v1'

    def query(self):
        response = self.get_route()
        return response

    def get_route(self):
        origin = self.parameters['origin']
        destination = self.parameters['destination']
        arrival_time = self.parameters['arrival_time']
        response = requests.get(f'{self.base_url}/maps/route?origin={origin}&'
                                f'destination={destination}&arrival_time={arrival_time}')
        return response.json()
