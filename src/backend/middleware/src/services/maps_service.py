import werkzeug  # Fix ImportError: cannot import name 'cached_property'
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Namespace, Resource

ns = Namespace('maps', description='Maps-Service')


@ns.route('/')
class GetMaps(Resource):
    def get(self):
        return
