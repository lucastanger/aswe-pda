import json
import yaml

import requests
import werkzeug  # Fix ImportError: cannot import name 'cached_property'

werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Resource, Namespace

ns = Namespace('swagger', description='Swagger APIs')

url = 'http://localhost:5000/rest/api/v1/swagger.json'


@ns.route('/swagger.yml')
class GetSwagger(Resource):
    def get(self):
        response = requests.get(url)
        data = json.loads(response.content)
        with open('docs/swagger.yml', 'w') as f:
            yaml.dump(data, f, allow_unicode=True)
        return {"message": "Yaml document generated!"}


@ns.route('/swagger.json')
class GetSwagger(Resource):
    def get(self):
        response = requests.get(url)
        data = json.loads(response.content)
        with open('docs/swagger.json', 'w') as f:
            json.dump(data, f)
        return {"message": "Json document generated!"}
