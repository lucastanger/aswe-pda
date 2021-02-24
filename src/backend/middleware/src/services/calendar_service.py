import werkzeug  # Fix ImportError: cannot import name 'cached_property'
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Namespace, Resource

ns = Namespace('calendar', description='Calendar-Service')


@ns.route('/')
class GetCalendar(Resource):
    def get(self):
        return
