from flask import Blueprint
from googleapiclient.discovery import build

import datetime
import json

from src.authentication import authenticate

events_api = Blueprint('events_api', __name__)


@events_api.route("/today", methods=['GET'])
def get_events_today():
    credentials = authenticate()

    service = build('calendar', 'v3', credentials=credentials)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    print(json.dumps(events, indent=4))

    return json.dumps(events)
