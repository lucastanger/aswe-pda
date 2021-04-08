# Imports.
from flask_restful import Resource, reqparse
from dotenv import load_dotenv
from os import getenv
import requests
import json


class Daily(Resource):
    """
    Includes GET Method for the last 100 days stock information.
    GET can return information about stock for the last 100 days.
    """

    def __init__(self):
        """
        Load api key and endpoint for alpha vantage.
        """

        # Load environment variables
        load_dotenv("./.secrets/stock-service.env")

    def get(self):
        """
        GET Method for returning information about a stock for the last 100 days.
        Receives a symbol in query parameters.
        Returns information about a stock like open, high, low, ... for the last 100 days.
        See swagger for more information.
        """

        # Extract argument from get request
        parser = reqparse.RequestParser()
        parser.add_argument("symbol", required=True, location="args")
        args = parser.parse_args(strict=True)

        # Create url for alpha vantage
        url = (
            getenv("STOCK_ENDPOINT")
            + "?function=TIME_SERIES_DAILY&symbol="
            + args["symbol"]
            + "&outputsize=full"
            + "&apikey="
            + getenv("STOCK_API_KEY")
        )

        # Send request to alpha vantage
        response_alpha_vantage = requests.get(url)

        # Get json from alpha vantage response
        json_alpha_vantage = response_alpha_vantage.json()

        # Check if api throwed error
        if "Note" in json_alpha_vantage:
            response_error = {
                "info": "Internal server error caused by third party api.",
                "error": json_alpha_vantage["Note"],
            }
            return response_error, 500

        if "Error Message" in json_alpha_vantage:
            response_error = {
                "info": "Internal server error caused by third party api.",
                "error": json_alpha_vantage["Error Message"],
            }
            return response_error, 500

        # Return response
        return json_alpha_vantage, 200
