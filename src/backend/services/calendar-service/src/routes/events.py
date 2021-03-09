from flask import make_response, jsonify
from flask_restplus import Namespace, Resource
from googleapiclient.discovery import build

import datetime
import json

from src.authentication import authenticate

ns = Namespace('events', description='Dialogflow APIs')


@ns.route('/')
@ns.route('/<date>')
class Events(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    def get(self, date=None):
        if date is None:
            date = self.date_now
        # Get credentials and initialize service
        credentials = authenticate()
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
