from src.util.mongodb import MongoDB
import requests


class DualisService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://dualis-service:5550/rest/api/v1'

    def query(self):

        # Load dualis login data from config
        config = (
            MongoDB.instance()
            .db['configuration']
            .find_one({'dualis': {'$exists': True},})
        )

        username = config['dualis']['_username']
        password = config['dualis']['_password']

        # Get grades from dualis api
        response = requests.get(
            f'{self.base_url}/grades', json={'user': username, 'password': password}
        )

        # Return response
        return response.json()
