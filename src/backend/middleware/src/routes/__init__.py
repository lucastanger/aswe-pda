from flask_restx import Api
from .swagger import ns as swagger_ns
from .dialogflow import ns as dialogflow_ns
from .authorization import ns as authorization_ns
from .configuration import ns as configuration_ns
from .t2ss2t import ns as t2ss2t_ns

api = Api(
    title='REST-API for Middleware',
    version='1.0.0',
    description='Middleware to connect frontend with backend.',
    prefix='/rest/api/v1',
    doc='/rest/api/v1/docs',
)

api.add_namespace(swagger_ns)
api.add_namespace(dialogflow_ns)
api.add_namespace(authorization_ns)
api.add_namespace(configuration_ns)
api.add_namespace(t2ss2t_ns)
