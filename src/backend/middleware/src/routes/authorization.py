import requests
from flask import url_for, request
from flask_restx import Resource, Namespace, fields

ns = Namespace('authorization', description='Authorization APIs')


@ns.route('/calendar-service')
class CalendarService(Resource):
    success_model = ns.model(
        'Calendar service authorization response - success',
        {'authorization_url': fields.String},
    )

    error_model = ns.model(
        'Calendar service authorization response - error', {'error': fields.String}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://calendar-service:5560/rest/api/v1'

    @ns.response(200, 'OK', success_model)
    @ns.response(400, 'Error', error_model)
    @ns.doc(description='Authorize with google.')
    def get(self):
        authorization_callback = url_for('authorization_calendar_service_callback')
        redirect_uri = f'http://localhost:5600{authorization_callback}'
        response = requests.get(
            f'{self.base_url}/authorization', params={'redirect_uri': redirect_uri}
        )
        return response.json()


@ns.route('/calendar-service/oauth2callback')
class CalendarServiceCallback(Resource):
    success_model = ns.model(
        'Calendar service callback response - success', {'message': fields.String}
    )

    error_model = ns.model(
        'Calendar service callback response - error', {'error': fields.String}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://calendar-service:5560/rest/api/v1'

    @ns.response(200, 'OK', success_model)
    @ns.response(400, 'Error', error_model)
    @ns.doc(description='Callback to be called after authentication.')
    def get(self):
        authorization_callback = url_for('authorization_calendar_service_callback')
        redirect_uri = f'http://localhost:5600{authorization_callback}'
        params = {'redirect_uri': redirect_uri, **request.args.to_dict()}
        response = requests.get(
            f'{self.base_url}/authorization/oauth2callback', params=params
        )
        return response.json()


@ns.route('/calendar-service/revoke')
class CalendarServiceRevoke(Resource):
    success_model = ns.model(
        'Calendar service revoke response - success', {'message': fields.String}
    )

    error_model = ns.model(
        'Calendar service revoke response - error', {'error': fields.String}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://calendar-service:5560/rest/api/v1'

    @ns.response(200, 'OK', success_model)
    @ns.response(400, 'Error', error_model)
    @ns.doc(description='Revoke the permissions.')
    def get(self):
        response = requests.get(f'{self.base_url}/authorization/revoke')
        return response.json()


@ns.route('/calendar-service/clear')
class CalendarServiceClear(Resource):
    success_model = ns.model(
        'Calendar service clear response - success', {'message': fields.String}
    )

    error_model = ns.model(
        'Calendar service clear response - error', {'error': fields.String}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://calendar-service:5560/rest/api/v1'

    @ns.response(200, 'OK', success_model)
    @ns.response(400, 'Error', error_model)
    @ns.doc(
        description='Clear all authentication data, if you want to completely remove the '
        'permissions, call /authorization/calendar-service/revoke first.'
    )
    def get(self):
        response = requests.get(f'{self.base_url}/authorization/clear')
        return response.json()


@ns.route('/spotify-service')
class SpotifyService(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://spotify-service:5565/rest/api/v1'

    def get(self):
        response = requests.get(f'{self.base_url}/spotify/auth')
        return response.json()


@ns.route('/spotify-service/oauth2callback')
class SpotifyServiceCallback(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://spotify-service:5565/rest/api/v1'

    def get(self):
        params = {**request.args.to_dict()}
        response = requests.get(f'{self.base_url}/spotify/callback', params=params)
        return response.json()
