from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from pymongo import MongoClient
import requests
import json

ns = Namespace('configuration', description='Configuration APIs')

client = MongoClient(host='mongo', port=27017)
db = client['aswe-pda']
db.authenticate('dev', 'dev')
configuration = db['configuration']


@ns.route('/')
class ConfigurationService(Resource):
    get_success_model = ns.model(
        'Configuration get response - success',
        {
            'general': fields.Raw({}),
            'dualis': fields.Raw({}),
            'news': fields.Raw({}),
            'weather': fields.Raw({}),
            'stocks': fields.Raw({}),
        },
    )

    get_error_model = ns.model(
        'Configuration get response - error', {'error': fields.String}
    )

    post_success_model = ns.model(
        'Configuration post response - success', {'message': fields.String},
    )

    post_error_model = ns.model(
        'Configuration post response - error', {'error': fields.String}
    )

    @ns.response(200, 'OK', get_success_model)
    @ns.response(400, 'Error', get_error_model)
    @ns.doc(description='Get configuration json.')
    def get(self):
        response = configuration.find_one(
            {
                'general': {'$exists': True},
                'dualis': {'$exists': True},
                'news': {'$exists': True},
                'weather': {'$exists': True},
                'stocks': {'$exists': True},
            }
        )
        del response['_id']
        return make_response(jsonify(response), 200)

    @ns.response(200, 'OK', post_success_model)
    @ns.response(400, 'Error', post_error_model)
    @ns.doc(description='Post configuration json.')
    def post(self):
        configuration.replace_one(
            {
                'general': {'$exists': True},
                'dualis': {'$exists': True},
                'news': {'$exists': True},
                'weather': {'$exists': True},
                'stocks': {'$exists': True},
            },
            request.json,
            upsert=True,
        )
        return make_response(
            {'message': 'Configuration successfully added or updated'}, 200
        )


@ns.route('/stock-service/symbol')
class StockService(Resource):
    @ns.doc(description='Get stock symbol by keyword.')
    def get(self):
        print(request.args)
        print(json.dumps(request.args))
        response = requests.get(
            'http://stock-service:5585/rest/api/v1/symbol',
            params={'keyword': request.args['keyword']},
        )

        return make_response(response.json(), 200)
