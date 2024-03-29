import os

import requests
from flask import request, make_response
from flask_restx import Resource, Namespace, fields
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

ns = Namespace('authorization', description='Google authentication APIs')

SCOPES = [
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid',
]
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v2'

# When running locally, disable OAuthlib's HTTPs verification
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


@ns.route('/')
class Authorize(Resource):
    success_model = ns.model(
        'Calendar service authorization response - success',
        {'authorization_url': fields.String},
    )

    error_model = ns.model(
        'Calendar service authorization response - error', {'error': fields.String}
    )

    @staticmethod
    @ns.response(200, 'OK', success_model)
    @ns.response(400, 'Error', error_model)
    @ns.doc(description='Authorize with google.')
    def get():
        flow = Flow.from_client_secrets_file('.secrets/credentials.json', SCOPES)

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
            include_granted_scopes='true',
        )

        # Store the state so the callback can verify the auth server response.
        MongoDB.instance().authorization.replace_one(
            {'service': 'calendar-service', 'type': 'state'},
            {'service': 'calendar-service', 'type': 'state', 'state': state},
            upsert=True,
        )

        return {'authorization_url': authorization_url}


@ns.route('/oauth2callback')
class Callback(Resource):
    success_model = ns.model('Callback response - success', {'message': fields.String})

    error_model = ns.model('Callback response - error', {'error': fields.String})

    @staticmethod
    @ns.response(200, 'OK', success_model)
    @ns.response(400, 'Error', error_model)
    @ns.doc(description='Callback to be called after authentication.')
    def get():
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.
        result = MongoDB.instance().authorization.find_one(
            {'service': 'calendar-service', 'type': 'state'}
        )
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
        MongoDB.instance().authorization.replace_one(
            {'service': 'calendar-service', 'type': 'credentials'},
            credentials_to_dict(credentials),
            upsert=True,
        )

        return make_response({'message': 'Successfully authorized.'}, 200)


@ns.route('/revoke')
class Revoke(Resource):
    success_model = ns.model('Revoke response - success', {'message': fields.String})

    error_model = ns.model('Revoke response - error', {'error': fields.String})

    @staticmethod
    @ns.response(200, 'OK', success_model)
    @ns.response(400, 'Error', error_model)
    @ns.doc(description='Revoke the permissions.')
    def get():
        result = MongoDB.instance().authorization.find_one(
            {'service': 'calendar-service', 'type': 'credentials'}
        )
        if result is None:
            return 'You need to authorize before revoking credentials.'

        credentials = Credentials(**document_to_dict(result))

        revoke = requests.post(
            'https://oauth2.googleapis.com/revoke',
            params={'token': credentials.token},
            headers={'content-type': 'application/x-www-form-urlencoded'},
        )

        status_code = getattr(revoke, 'status_code')
        if status_code == 200:
            return make_response({'message': 'Credentials successfully revoked.'}, 200)
        else:
            return make_response({'error': 'An error occurred.'}, 400)


@ns.route('/clear')
class Clear(Resource):
    success_model = ns.model('Clear response - success', {'message': fields.String})

    error_model = ns.model('Clear response - error', {'error': fields.String})

    @staticmethod
    @ns.response(200, 'OK', success_model)
    @ns.response(400, 'Error', error_model)
    @ns.doc(
        description='Clear all authentication data, if you want to completely remove the '
        'permissions, call /authorization/revoke first.'
    )
    def get():
        MongoDB.instance().authorization.delete_many({'service': 'calendar-service'})
        return make_response({'message': 'Credentials have been cleared.'}, 200)


def credentials_to_dict(credentials):
    """
    Convert credentials from google to dict.
    :param credentials: Credentials from google_auth_oauthlib.flow.
    :return: Credentials as dict.
    """
    return {
        'service': 'calendar-service',
        'type': 'credentials',
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }


def document_to_dict(document):
    """
    Convert document from mongodb to dict, so that it can be used with google.oauth2.credentials.
    :param document: Document from mongodb.
    :return: Document as dict.
    """
    return {
        'token': document['token'],
        'refresh_token': document['refresh_token'],
        'token_uri': document['token_uri'],
        'client_id': document['client_id'],
        'client_secret': document['client_secret'],
        'scopes': document['scopes'],
    }


def get_credentials():
    """
    Get the credentials from the mongodb.
    :return: Credentials from mongodb.
    """
    document = MongoDB.instance().authorization.find_one(
        {'service': 'calendar-service', 'type': 'credentials'}
    )
    if document is None:
        return make_response({'error': 'You are not authenticated.'}, 401), False
    return document_to_dict(document), True


class MongoDB:
    """
    Creates a connection to the mongodb.
    """

    __instance = None

    def __init__(self):
        try:
            client = MongoClient(
                host='mongo', port=27017, serverSelectionTimeoutMS=1000
            )
            client.server_info()
        except ServerSelectionTimeoutError:
            client = MongoClient(
                host='localhost', port=27017, serverSelectionTimeoutMS=1000
            )
            client.server_info()
        db = client['aswe-pda']
        db.authenticate('dev', 'dev')
        self.authorization = db['authorization']

    @classmethod
    def instance(cls):
        """
        Returns a singleton instance of this class. Upon its first call, a new instance
        is being created. On all subsequent calls, the already created instance is returned.
        """
        if cls.__instance:
            return cls.__instance
        else:
            cls.__instance = MongoDB()
            return cls.__instance
