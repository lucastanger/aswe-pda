import werkzeug  # Fix ImportError: cannot import name 'cached_property'
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Namespace, Resource

ns = Namespace('weather', description='Weather-Service')


@ns.route('/')
class GetWeather(Resource):
    def get(self):
        return
