import werkzeug  # Fix ImportError: cannot import name 'cached_property'
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Api
from .swagger import ns as swagger_ns
from .dialogflow import ns as dialogflow_ns

api = Api(
    title='REST-API for Middleware',
    version='1.0.0',
    description='Middleware to connect frontend with backend',
    prefix='/rest/api/v1',
    doc='/rest/api/v1/docs'
)

api.add_namespace(swagger_ns)
api.add_namespace(dialogflow_ns)
