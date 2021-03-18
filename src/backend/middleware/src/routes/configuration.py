from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from pymongo import MongoClient

ns = Namespace('configuration', description='Configuration APIs')

client = MongoClient(host='mongo', port=27017)
db = client['aswe-pda']
db.authenticate('dev', 'dev')
configuration = db['configuration']


@ns.route('/')
class CalendarService(Resource):
    get_success_model = ns.model(
        'Configuration get response - success',
        {'general': fields.Raw({}),
         'dualisService': fields.Raw({}),
         'newsService': fields.Raw({}),
         'weatherService': fields.Raw({}),
         'stocksService': fields.Raw({})},
    )

    get_error_model = ns.model(
        'Configuration get response - error',
        {'error': fields.String}
    )

    post_success_model = ns.model(
        'Configuration post response - success',
        {'message': fields.String},
    )

    post_error_model = ns.model(
        'Configuration post response - error',
        {'error': fields.String}
    )

    @ns.response(200, 'OK', get_success_model)
    @ns.response(400, 'Error', get_error_model)
    @ns.doc(description='Get configuration json.')
    def get(self):
        response = configuration.find_one({
            'general': {'$exists': True},
            'dualisService': {'$exists': True},
            'newsService': {'$exists': True},
            'weatherService': {'$exists': True},
            'stocksService': {'$exists': True}}
        )
        del response['_id']
        return make_response(jsonify(response), 200)

    @ns.response(200, 'OK', post_success_model)
    @ns.response(400, 'Error', post_error_model)
    @ns.doc(description='Post configuration json.')
    def post(self):
        configuration.replace_one({
            'general': {'$exists': True},
            'dualisService': {'$exists': True},
            'newsService': {'$exists': True},
            'weatherService': {'$exists': True},
            'stocksService': {'$exists': True}},
            request.json,
            upsert=True,
        )
        return make_response({'message': 'Configuration successfully added or updated'}, 200)
