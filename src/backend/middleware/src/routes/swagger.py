import json

import requests
import yaml
from flask import request
from flask_restx import Resource, Namespace

ns = Namespace('swagger', description='Swagger APIs')


@ns.route('/swagger.yml')
class Swagger(Resource):
    @staticmethod
    @ns.response(200, 'OK')
    @ns.doc(description='Generate a swagger.yml file.')
    def get():
        url = f'{request.url_root}/rest/api/v1/swagger.json'
        response = requests.get(url)
        data = json.loads(response.content)
        with open('docs/swagger.yml', 'w') as f:
            yaml.dump(data, f, allow_unicode=True)
        return {'message': 'Yaml document generated!'}
