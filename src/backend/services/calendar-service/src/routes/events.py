import datetime
import json

from flask import make_response, jsonify
from flask_restx import Namespace, Resource
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.routes.authorization import get_credentials

ns = Namespace('events', description='Google calendar events APIs')


@ns.route('/', endpoint="events_endpoint")
@ns.route('/<date>')
class Events(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    def get(self, date=None):
        if date is None:
            date = self.date_now

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
                maxResults=10,
                singleEvents=True,
                orderBy='startTime',
            )
                .execute()
        )
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        print(json.dumps(events, indent=4))

        return make_response(jsonify(events), 200)
