import datetime
import os
from os.path import dirname, join

import googlemaps
from dotenv import load_dotenv
from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace, reqparse, fields

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
class MapsRoute(Resource):
    success_model = ns.model('Maps service route response - success', {})

    error_model = ns.model(
        'Maps service route response - error', {'error': fields.Raw({})}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_now = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    @ns.response(200, 'OK', success_model)
    @ns.response(400, 'Error', error_model)
    @ns.doc(
        description='Get a route from origin to destination with a optional arrival time.'
    )
    def get(self):
        if ('origin' not in request.args or 'destination' not in request.args) or (
            not request.args.get('origin') or not request.args.get('destination')
        ):
            return make_response(
                {'error': 'Not all required arguments specified (origin, destination)'},
                400,
            )

        origin = request.args.get('origin')
        destination = request.args.get('destination')
        arrival_time = request.args.get('arrival_time')
        gmaps = googlemaps.Client(key=os.getenv('API_KEY'))

        # Request directions
        if 'arrival_time' not in request.args or not request.args.get('arrival_time'):
            print(self.date_now)
            directions_result = gmaps.directions(
                origin,
                destination,
                # mode='transit',
                # departure_time=self.date_now,
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
