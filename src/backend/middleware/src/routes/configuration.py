import requests
from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields

from src.util.mongodb import MongoDB

ns = Namespace('configuration', description='Configuration APIs')


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
        response = MongoDB.instance().db['configuration'].find_one(
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
        MongoDB.instance().db['configuration'].replace_one(
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
        response = requests.get(
            'http://stock-service:5585/rest/api/v1/symbol',
            params={'keyword': request.args['keyword']},
        )

        return make_response(response.json(), 200)
