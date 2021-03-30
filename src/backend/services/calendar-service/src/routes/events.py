import datetime

import pytz
from flask import make_response, jsonify
from flask_restx import Namespace, Resource
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.routes.authorization import get_credentials

ns = Namespace('events', description='Google calendar events APIs')


@ns.route('/')
@ns.route('/<date>')
class Events(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_now = (
            datetime.datetime.utcnow()
            .astimezone(pytz.timezone('Europe/Berlin'))
            .strftime('%Y-%m-%dT%H:%M:%S%z')
        )

    @ns.response(200, 'OK')
    @ns.response(400, 'Error')
    @ns.doc(
        description='Get events with specified date, if no date is specified, the current '
        'date is used.'
    )
    def get(self, date=None):
        if date is None:
            date = self.date_now

        try:
            max_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            return make_response({'error': 'Invalid date.'}, 400)
        max_date = max_date.replace(
            hour=23, minute=59, second=59, microsecond=0
        ).astimezone(pytz.timezone('Europe/Berlin'))
        max_date = max_date.strftime('%Y-%m-%dT%H:%M:%S%z')

        # Load credentials from the session.
        result, success = get_credentials()
        if not success:
            return result
        credentials = Credentials(**result)

        service = build('calendar', 'v3', credentials=credentials)

        # Call the Calendar API
        events_result = (
            service.events()
            .list(
                calendarId='primary',
                timeMin=date,
                timeMax=max_date,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime',
            )
            .execute()
        )
        events = events_result.get('items', [])

        if not events:
            return make_response({'message': 'No upcoming events found.'}, 200)

        return make_response(jsonify(events), 200)
