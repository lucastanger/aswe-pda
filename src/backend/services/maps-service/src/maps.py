from flask import jsonify, request, make_response
from dotenv import load_dotenv
from os.path import dirname, join

import googlemaps
import os
import datetime
import pytz
import werkzeug  # Fix ImportError: cannot import name 'cached_property'

werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Resource, Namespace, reqparse

project_root = dirname(dirname(__file__))
output_path = join(project_root, '.secrets/.env')
load_dotenv(output_path)

ns = Namespace('maps', description='Maps APIs')

parser = reqparse.RequestParser()
parser.add_argument('origin', type=str, help='Start location of the route')
parser.add_argument('destination', type=str, help='Destination location of the route')
parser.add_argument('arrival_time', type=str, help='Desired arrival time')


# https://googlemaps.github.io/google-maps-services-python/docs/index.html
# https://developers.google.com/maps/documentation/javascript/directions#RenderingDirections
@ns.route('/route')
@ns.response(200, 'Success')
@ns.response(
    400, 'not all required arguments specified (origin, destination, arrival_time)'
)
@ns.expect(parser)
class GetMapsRoute(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_now = datetime.datetime.utcnow().astimezone(
            pytz.timezone('Europe/Berlin')
        )

    def get(self):
        if ('origin' not in request.args or 'destination' not in request.args) or (
            not request.args.get('origin') or not request.args.get('destination')
        ):
            return make_response(
                {
                    'error': 'Not all required arguments specified (origin, '
                    'destination, arrival_time)'
                },
                400,
            )

        origin = request.args.get('origin')
        destination = request.args.get('destination')
        arrival_time = request.args.get('arrival_time')
        gmaps = googlemaps.Client(key=os.getenv('API_KEY'))

        # Request directions
        if 'arrival_time' not in request.args or not request.args.get('arrival_time'):
            directions_result = gmaps.directions(
                origin,
                destination,
                # mode='transit',
                departure_time=self.date_now,
                units='metric',
            )
        else:
            directions_result = gmaps.directions(
                origin,
                destination,
                arrival_time=arrival_time,
                # mode='transit',
                units='metric',
            )

        return make_response(jsonify(directions_result), 200)
