from flask import jsonify
from flask_restful import Resource, reqparse


class Synthesize(Resource):

    def post(self):
        # Extract text from body
        parser = reqparse.RequestParser()
        parser.add_argument('text', required=True, location='json')
        args = parser.parse_args(strict=True)
        text = args['text']

        # Synthesize

        return jsonify(args['text'])
