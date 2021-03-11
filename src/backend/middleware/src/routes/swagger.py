import json

import requests
import yaml
from flask import request
from flask_restx import Resource, Namespace

ns = Namespace('swagger', description='Swagger APIs')


@ns.route('/swagger.yml')
class Swagger(Resource):
    @staticmethod
    def get():
        url = f'{request.url_root}/rest/api/v1/swagger.json'
        response = requests.get(url)
        data = json.loads(response.content)
        with open('docs/swagger.yml', 'w') as f:
            yaml.dump(data, f, allow_unicode=True)
        return {'message': 'Yaml document generated!'}


@ns.route('/swagger.json')
class Swagger(Resource):
    @staticmethod
    def get():
        url = f'{request.url_root}/rest/api/v1/swagger.json'
        response = requests.get(url)
        data = json.loads(response.content)
        with open('docs/swagger.json', 'w') as f:
            json.dump(data, f)
        return {'message': 'Json document generated!'}
