import datetime

import pytz
import requests


class CalendarService:
    """
    Responsible for the communication between dialogflow and the calendar service.
    """

    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://calendar-service:5560/rest/api/v1'

    def query(self):
        """
        Query the response from dialogflow.
        :return: Response from the calendar service.
        """
        if self.parameters['calendar-alarm']:
            response = self.get_next_event()
        else:
            response = self.get_events()
        return response

    def get_events(self):
        """
        Get all events at the specified date.
        :return: Events at the specified date, returns a message, if no events have been found.
        """
        date = self.parameters['date']
        response = requests.get(f'{self.base_url}/events/{date}')
        return response.json()

    def get_next_event(self):
        """
        Get the next event of the following day.
        :return: First event of the following day.
        """
        date_tomorrow = (
            datetime.datetime.utcnow().astimezone(pytz.timezone('Europe/Berlin'))
            + datetime.timedelta(days=1)
        ).replace(
            hour=0, minute=0, second=0
        ).strftime('%Y-%m-%dT%H:%M:%S%z')
        response = requests.get(f'{self.base_url}/events/{date_tomorrow}')
        if 'message' in response.json():
            return {'message': 'No upcoming events for tomorrow found.'}
        return response.json()[0]
