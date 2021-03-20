from pymongo import MongoClient
import requests
from flask import jsonify

client = MongoClient(host='mongo', port=27017)
db = client['aswe-pda']
db.authenticate('dev', 'dev')
configuration = db['configuration']


class StockService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://stock-service:5585/rest/api/v1'

    def query(self):

        # No stock is given. Take stock from config
        if not self.parameters['stock']:
            # Load config
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

            stock = config['stocksService']['stocks']
        else:
            stock = self.parameters['stock']

        # Get symbol
        response_symbols = self.get_symbol(stock)

        # No matches found
        if not response_symbols:
            return {'error': 'Stock not found.'}

        response_symbol = response_symbols.json()

        # Check if today is given.
        if self.parameters['date']:
            response = self.get_today(response_symbol['bestMatches'][0]['1. symbol'])
        else:
            response = self.get_daily(response_symbol['bestMatches'][0]['1. symbol'])

        return response.json()

    def get_today(self, stock):
        # Make request /today
        response = requests.get(f'{self.base_url}/today', params={'symbol': stock})
        return response

    def get_daily(self, stock):
        # Make request /daily
        response = requests.get(f'{self.base_url}/daily', params={'symbol': stock})
        return response

    def get_symbol(self, stock):
        # Make request /symbol
        response = requests.get(f'{self.base_url}/symbol', params={'keyword': stock})
        return response
