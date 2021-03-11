import os

import requests
from flask import request, make_response
from flask_restx import Resource, Namespace
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from pymongo import MongoClient

ns = Namespace('authorization', description='Google authentication APIs')

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v2'

# When running locally, disable OAuthlib's HTTPs verification
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client = MongoClient(host='mongo', port=27017)
db = client['aswe-pda']
db.authenticate('dev', 'dev')
authorization = db['authorization']


@ns.route('/')
class Authorize(Resource):
    @staticmethod
    def get():
        flow = Flow.from_client_secrets_file(
            '.secrets/credentials.json', SCOPES
        )

        # The URI created here must exactly match one of the authorized redirect URIs
        # for the OAuth 2.0 client, which you configured in the API Console. If this
        # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
        # error.
        flow.redirect_uri = request.args.get('redirect_uri')

        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')

        # Store the state so the callback can verify the auth server response.
        authorization.replace_one({'service': 'calendar-service', 'type': 'state'},
                                  {'service': 'calendar-service', 'type': 'state',
                                  'state': state}, upsert=True)

        return {'authorization_url': authorization_url}


@ns.route('/oauth2callback')
class Callback(Resource):
    @staticmethod
    def get():
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.
        result = authorization.find_one({'service': 'calendar-service', 'type': 'state'})
        state = result['state']

        flow = Flow.from_client_secrets_file(
            '.secrets/credentials.json', SCOPES, state=state
        )
        flow.redirect_uri = request.args.get('redirect_uri')

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)

        # Store credentials in mongo.
        credentials = flow.credentials
        authorization.replace_one({'service': 'calendar-service', 'type': 'credentials'},
                                  credentials_to_dict(credentials), upsert=True)

        return make_response({'message': 'Successfully authorized.'}, 200)


@ns.route('/revoke')
class Revoke(Resource):
    @staticmethod
    def get():
        result = authorization.find_one({'service': 'calendar-service', 'type': 'credentials'})
        if result is None:
            return 'You need to authorize before revoking credentials.'

        credentials = Credentials(**document_to_dict(result))

        revoke = requests.post('https://oauth2.googleapis.com/revoke',
                               params={'token': credentials.token},
                               headers={'content-type': 'application/x-www-form-urlencoded'})

        status_code = getattr(revoke, 'status_code')
        if status_code == 200:
            return make_response({'message': 'Credentials successfully revoked.'}, 200)
        else:
            return make_response({'error': 'An error occurred.'}, 400)


@ns.route('/clear')
class Clear(Resource):
    @staticmethod
    def get():
        authorization.delete_many({'service': 'calendar-service'})
        return make_response({'message': 'Credentials have been cleared.'}, 200)


def credentials_to_dict(credentials):
    return {
        'service': 'calendar-service',
        'type': 'credentials',
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


def document_to_dict(document):
    return {
        'token': document['token'],
        'refresh_token': document['refresh_token'],
        'token_uri': document['token_uri'],
        'client_id': document['client_id'],
        'client_secret': document['client_secret'],
        'scopes': document['scopes']
    }


def get_credentials():
    document = authorization.find_one({'service': 'calendar-service', 'type': 'credentials'})
    if document is None:
        return make_response({'error': 'You are not authenticated.'}, 401), False
    return document_to_dict(document), True
