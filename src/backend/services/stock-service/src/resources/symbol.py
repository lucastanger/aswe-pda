# Imports.
from flask_restful import Resource, reqparse
from dotenv import load_dotenv
from os import getenv
import requests
import json


class Symbol(Resource):
    """
    Includes GET Method for returning a stock symbol.
    GET can return stock symbols by given keyword.
    """

    def __init__(self):
        """
        Load api key and endpoint for alpha vantage.
        """

        # Load environment variables
        load_dotenv('./.secrets/stock-service.env')

    def get(self):
        """
        GET Method for returning a stock symbol.
        Receives a keyword in query parameters.
        Returns a list of matching symbols as well meta data.
        See swagger for more information.
        """

        # Extract argument from get request
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', required=True, location='args')
        args = parser.parse_args(strict=True)

        # Create url for alpha vantage
        url = (
            getenv('STOCK_ENDPOINT')
            + '?function=SYMBOL_SEARCH&keywords='
            + args['keyword']
            + '&apikey='
            + getenv('STOCK_API_KEY')
        )

        # Send request to alpha vantage
        response_alpha_vantage = requests.get(url)

        # Get json from alpha vantage response
        json_alpha_vantage = response_alpha_vantage.json()

        # Check if api throwed error
        if 'Note' in json_alpha_vantage:
            response_error = {
                'info': 'Internal server error caused by third party api.',
                'error': json_alpha_vantage['Note'],
            }
            return response_error, 500

        if 'Error Message' in json_alpha_vantage:
            response_error = {
                'info': 'Internal server error caused by third party api.',
                'error': json_alpha_vantage['Error Message'],
            }
            return response_error, 500

        # Check if matches are found
        if not len(json_alpha_vantage['bestMatches']):
            response_error = {'error': 'No matches found.'}
            return response_error, 400

        # Return response
        return json_alpha_vantage, 200
