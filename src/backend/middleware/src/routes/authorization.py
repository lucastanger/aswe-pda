import requests
from flask import redirect, url_for, request
from flask_restx import Resource, Namespace

ns = Namespace('authorization', description='Authorization APIs')


@ns.route('/calendar-service')
class CalendarService(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://calendar-service:5560/rest/api/v1'

    def get(self):
        authorization_callback = url_for('authorization_calendar_service_callback')
        redirect_uri = f'http://localhost:5600{authorization_callback}'
        response = requests.get(
            f'{self.base_url}/authorization', params={'redirect_uri': redirect_uri}
        )
        authorization_url = response.json()['authorization_url']
        return redirect(authorization_url)


@ns.route('/calendar-service/oauth2callback')
class CalendarServiceCallback(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://calendar-service:5560/rest/api/v1'

    def get(self):
        authorization_callback = url_for('authorization_calendar_service_callback')
        redirect_uri = f'http://localhost:5600{authorization_callback}'
        params = {'redirect_uri': redirect_uri, **request.args.to_dict()}
        response = requests.get(
            f'{self.base_url}/authorization/oauth2callback', params=params
        )
        return response.json()


@ns.route('/calendar-service/revoke')
class CalendarServiceCallback(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://calendar-service:5560/rest/api/v1'

    def get(self):
        response = requests.get(
            f'{self.base_url}/authorization/revoke'
        )
        return response.json()


@ns.route('/calendar-service/clear')
class CalendarServiceCallback(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'http://calendar-service:5560/rest/api/v1'

    def get(self):
        response = requests.get(
            f'{self.base_url}/authorization/clear'
        )
        return response.json()
