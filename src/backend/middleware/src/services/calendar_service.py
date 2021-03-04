import requests


class CalendarService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://calendar-service:5560/rest/api/v1'

    def query(self):
        response = self.get_events()
        return response

    def get_events(self):
        response = requests.get(f'{self.base_url}/events/today',
                                params={'date': self.parameters['date']})
        return response.json()
