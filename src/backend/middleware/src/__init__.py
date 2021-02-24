import werkzeug  # Fix ImportError: cannot import name 'cached_property'
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Api
from .swagger import ns as swagger_ns
from .services.calendar_service import ns as calendar_ns
from .services.dualis_service import ns as dualis_ns
from .services.maps_service import ns as maps_ns
from .services.news_service import ns as news_ns
from .services.spotify_service import ns as spotify_ns
from .services.t2s_s2t_service import ns as t2s_s2t_ns
from .services.weather_service import ns as weather_ns

api = Api(
    title='REST-API for Middleware',
    version='1.0.0',
    description='Middleware to connect frontend with backend',
    prefix='/rest/api/v1',
    doc='/rest/api/v1/docs'
)

api.add_namespace(swagger_ns)

api.add_namespace(calendar_ns)
api.add_namespace(dualis_ns)
api.add_namespace(maps_ns)
api.add_namespace(news_ns)
api.add_namespace(spotify_ns)
api.add_namespace(t2s_s2t_ns)
api.add_namespace(weather_ns)
