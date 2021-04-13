import requests


class MapsService:
    """
    Responsible for the communication between dialogflow and the calendar service.
    """

    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://maps-service:5580/rest/api/v1'

    def query(self):
        """
        Query the response from dialogflow.
        :return: Response from the maps service.
        """
        response = self.get_route()
        return response

    def get_route(self):
        """
        Get a route from origin to destination with a optional arrival time. If no
        arrival time is been given, the current time will be taken as departure time.
        :return: Route from origin to destination.
        """
        origin = self.parameters['origin']
        destination = self.parameters['destination']
        arrival_time = self.parameters['arrival_time']
        response = requests.get(
            f'{self.base_url}/maps/route?origin={origin}&'
            f'destination={destination}&arrival_time={arrival_time}'
        )
        return response.json()
