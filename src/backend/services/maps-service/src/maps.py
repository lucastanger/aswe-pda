from flask import jsonify, request
from dotenv import load_dotenv
from os.path import dirname, join

import googlemaps
import os
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
    def get(self):
        if (
            'origin' not in request.args
            or 'destination' not in request.args
            or 'arrival_time' not in request.args
        ):
            ns.abort(
                400,
                'not all required arguments specified (origin, destination, arrival_time)',
            )
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        arrival_time = request.args.get('arrival_time')
        gmaps = googlemaps.Client(key=os.getenv('API_KEY'))

        # Request directions
        # now = datetime.now()
        directions_result = gmaps.directions(
            origin,
            destination,
            arrival_time=arrival_time,
            mode='transit',
            # departure_time=now,
            units='metric',
        )

        return jsonify(directions_result), 200
