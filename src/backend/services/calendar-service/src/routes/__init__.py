from flask_restx import Api
from .swagger import ns as swagger_ns
from .events import ns as events_ns
from .authorization import ns as authorization_ns

api = Api(
    title='REST-API for Calendar-Service',
    version='1.0.0',
    description='Service to receive appointments from google calendar',
    prefix='/rest/api/v1',
    doc='/rest/api/v1/docs',
)

api.add_namespace(swagger_ns)
api.add_namespace(events_ns)
api.add_namespace(authorization_ns)
