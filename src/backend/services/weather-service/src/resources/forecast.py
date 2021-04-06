# Imports.
from flask_restful import Resource, reqparse
from dotenv import load_dotenv
from os import getenv
import requests
import json


class Forecast(Resource):
    """
    Includes GET Method for the a weather forecast.
    GET can get information about the weather up to 17 days by city name or coordinates.
    """

    def __init__(self):
        """
        Load api key and endpoint for openweatherapi.
        """

        # Load environment variables.
        load_dotenv("./.secrets/weather-service.env")

    def get(self):
        """
        GET Method for the weather forecast.
        Receives city name or coordinates in query parameters.
        Also requires a valid unit.
        Also possible, days between 1 and 17 of how many you want to receive.
        Returns a weather forecast for your city name or coordinates.
        See swagger for more information.
        """

        # Extract arguments from get request
        parser = reqparse.RequestParser()
        parser.add_argument("city", location="args")
        parser.add_argument("lat", type=float, location="args")
        parser.add_argument("lon", type=float, location="args")
        parser.add_argument("days", type=int, location="args")
        parser.add_argument(
            "unit",
            required=True,
            choices=("metric", "imperial"),
            location="args",
            help="Invalid Unit: {error_msg}",
        )
        args = parser.parse_args(strict=True)

        # Check if get current weather by city name or coordinates
        if args["city"] and not (args["lat"] or args["lon"]):
            # Create url for openweather api
            url = (
                getenv("WEATHER_ENDPOINT")
                + "/forecast/daily?q="
                + args["city"]
                + "&cnt="
                + str(args["days"] if args["days"] else 8)
                + "&appid="
                + getenv("WEATHER_API_KEY")
                + "&units="
                + args["unit"]
            )
        elif args["lat"] and args["lon"] and not args["city"]:
            # Create url for openweather api
            url = (
                getenv("WEATHER_ENDPOINT")
                + "/forecast/daily?lat="
                + str(args["lat"])
                + "&lon="
                + str(args["lon"])
                + "&cnt="
                + str(args["days"] if args["days"] else 8)
                + "&appid="
                + getenv("WEATHER_API_KEY")
                + "&units="
                + args["unit"]
            )
        else:
            response_error = {"error": "Either `city` or `lat` and `lon` are required."}
            return response_error, 400

        # Send request to openweather api
        try:
            response_openweather = requests.get(url)
            response_openweather.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            response_error = {
                "info": "Internal server error caused by third party api.",
                "error": {
                    "code": response_openweather.status_code,
                    "message": response_openweather.reason,
                    "full_error": str(ex),
                },
            }
            return response_error, 500

        # Get json from openweather response
        json_openweather = response_openweather.json()

        # Create response json
        json_response = {
            "city_name": json_openweather["city"]["name"],
            "timezone": json_openweather["city"]["timezone"],
            "weather": [],
            "widget": (
                '<div id="openweathermap-widget-21"></div><script src="//openweathermap.org/themes/openweathermap/assets/vendor/owm/js/d3.min.js"></script><script>window.myWidgetParam ? window.myWidgetParam : window.myWidgetParam = [];  window.myWidgetParam.push({id: 21,cityid: "'
                + str(json_openweather["city"]["id"])
                + "\",appid: '"
                + getenv("WEATHER_API_KEY")
                + "',units: 'metric',containerid: 'openweathermap-widget-21',  });  (function() {var script = document.createElement('script');script.async = true;script.charset = "
                + '"utf-8";script.src = "//openweathermap.org/themes/openweathermap/assets/vendor/owm/js/weather-widget-generator.js";var s = document.getElementsByTagName('
                + "'script')[0];s.parentNode.insertBefore(script, s);  })();</script>"
            ),
        }

        for day in json_openweather["list"]:
            json_response["weather"].append(
                {
                    "main": day["weather"][0]["main"],
                    "description": day["weather"][0]["description"],
                    "icon": day["weather"][0]["icon"],
                    "cloudiness": day["clouds"],
                    "wind": {"speed": day["speed"], "deg": day["deg"]},
                    "rain": {
                        "volume": day["rain"] if "rain" in day else 0,
                        "probability": day["pop"],
                    },
                    "snow": day["snow"] if "snow" in day else 0,
                    "temp": {
                        "day": day["temp"]["day"],
                        "min": day["temp"]["min"],
                        "max": day["temp"]["max"],
                        "night": day["temp"]["night"],
                        "eve": day["temp"]["eve"],
                        "morn": day["temp"]["morn"],
                        "feels_like": day["feels_like"],
                    },
                    "time": {
                        "dt": day["dt"],
                        "sunrise": day["sunrise"],
                        "sunset": day["sunset"],
                    },
                }
            )

        # Return response
        return json_response, 200
