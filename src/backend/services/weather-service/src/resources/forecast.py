# Imports.
from flask_restful import Resource, reqparse
from dotenv import load_dotenv
from os import getenv
import requests
import json


class Forecast(Resource):
    def __init__(self):
        # Load environment variables.
        load_dotenv("weather-auth.env")

    def get(self):
        # Extract arguments from get request
        parser = reqparse.RequestParser()
        parser.add_argument("city", required=True, location="args")
        parser.add_argument("cnt", location="args")
        args = parser.parse_args(strict=True)

        # Create url for openweather api
        url = (
            getenv("WEATHER_ENDPOINT")
            + "/forecast/daily?q="
            + args["city"]
            + "&cnt="
            + str(args["cnt"] if args["cnt"] else 8)
            + "&appid="
            + getenv("WEATHER_API_KEY")
            + "&units=metric"
        )

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
        # json_response = {
        #     "city_name": json_openweather["name"],
        #     "weather": {
        #         "main": json_openweather["weather"][0]["main"],
        #         "description": json_openweather["weather"][0]["description"],
        #         "cloudiness": json_openweather["clouds"]["all"],
        #         "wind": {
        #             "speed": json_openweather["wind"]["speed"],
        #             "deg": json_openweather["wind"]["deg"],
        #         },
        #         "temp": {
        #             "current": json_openweather["main"]["temp"],
        #             "feels_like": json_openweather["main"]["feels_like"],
        #             "min": json_openweather["main"]["temp_min"],
        #             "max": json_openweather["main"]["temp_max"],
        #         },
        #     },
        #     "time": {
        #         "current": json_openweather["dt"],
        #         "timezone": json_openweather["timezone"],
        #         "sunrise": json_openweather["sys"]["sunrise"],
        #         "sunset": json_openweather["sys"]["sunset"],
        #     },
        #     "widget": (
        #         '<div id="openweathermap-widget-22"></div><script>window.myWidgetParam ? window.myWidgetParam : window.myWidgetParam = [];  window.myWidgetParam.push({id: 22,cityid: \''
        #         + str(json_openweather["id"])
        #         + "',appid: '"
        #         + getenv("WEATHER_API_KEY")
        #         + "',units: 'metric',containerid: 'openweathermap-widget-22',  });  (function() {var script = document.createElement('script');script.async = true;script.charset = \"utf-8\";script.src = \"//openweathermap.org/themes/openweathermap/assets/vendor/owm/js/weather-widget-generator.js\";var s = document.getElementsByTagName('script')[0];s.parentNode.insertBefore(script, s);  })();</script>"
        #     ),
        # }

        # Return response
        return json_response, 200
