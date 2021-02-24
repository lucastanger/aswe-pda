import werkzeug  # Fix ImportError: cannot import name 'cached_property'
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Namespace, Resource

ns = Namespace('t2s-s2t', description='T2s-S2t-Service')


@ns.route('/')
class GetT2sS2t(Resource):
    def get(self):
        return
