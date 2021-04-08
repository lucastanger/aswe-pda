# Imports.
from flask_restful import Resource, reqparse
from dotenv import load_dotenv
from os import getenv
import requests
import json


class Today(Resource):
    """
    Includes GET Method for returning the current values for a stock from today.
    GET can return information about stock from today.
    """

    def __init__(self):
        """
        Load api key and endpoint for alpha vantage.
        """

        # Load environment variables
        load_dotenv("./.secrets/stock-service.env")

    def get(self):
        """
        GET Method for returning current information about a stock.
        Receives a symbol in query parameters.
        Returns information about a stock like open, high, low, ....
        See swagger for more information.
        """

        # Extract argument from get request
        parser = reqparse.RequestParser()
        parser.add_argument("symbol", required=True, location="args")
        args = parser.parse_args(strict=True)

        # Create url for alpha vantage
        url = (
            getenv("STOCK_ENDPOINT")
            + "?function=GLOBAL_QUOTE&symbol="
            + args["symbol"]
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

        # Check if symbol is found
        if not "Global Quote" in json_alpha_vantage:
            response_error = {"error": "No symbol found."}
            return response_error, 400

        if not "01. symbol" in json_alpha_vantage["Global Quote"]:
            response_error = {"error": "No symbol found."}
            return response_error, 400

        # Create response json
        response_json = {"symbol": json_alpha_vantage["Global Quote"]}

        # Return response
        return response_json, 200
