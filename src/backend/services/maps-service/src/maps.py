from flask import Blueprint, jsonify, request
from datetime import datetime
from dotenv import load_dotenv
from os.path import dirname, join

import googlemaps
import os

maps_api = Blueprint('maps_api', __name__)
project_root = dirname(dirname(__file__))
output_path = join(project_root, '.secrets/.env')
load_dotenv(output_path)


# https://googlemaps.github.io/google-maps-services-python/docs/index.html
# https://developers.google.com/maps/documentation/javascript/directions#RenderingDirections
@maps_api.route("/direction", methods=['GET'])
def get_maps_direction():
    if 'origin' not in request.args or \
            'destination' not in request.args or \
            'arrival_time' not in request.args:
        return {'message': 'not all required arguments specified (origin, destination, '
                           'arrival_time)'}, 400
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    arrival_time = request.args.get('arrival_time')
    gmaps = googlemaps.Client(key=os.getenv('API_KEY'))

    # Request directions
    # now = datetime.now()
    directions_result = gmaps.directions(origin,
                                         destination,
                                         arrival_time=arrival_time,
                                         mode='transit',
                                         # departure_time=now,
                                         units='metric')

    return jsonify(directions_result), 200
