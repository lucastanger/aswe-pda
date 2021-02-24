import werkzeug  # Fix ImportError: cannot import name 'cached_property'
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Api
from .maps import ns as maps_ns
from .swagger import ns as swagger_ns

api = Api(
    title='REST-API for Maps-Service',
    version='1.0.0',
    description='Service to handle requests for the google maps api',
    prefix='/rest/api/v1',
    doc='/rest/api/v1/docs'
)

api.add_namespace(maps_ns)
api.add_namespace(swagger_ns)
