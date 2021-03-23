import base64, json, sys, requests

from flask import make_response
from pymongo import MongoClient

try:
    import urllib.request, urllib.error
    import urllib.parse as urllibparse
except ImportError:
    import urllib as urllibparse

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
RESPONSE_TYPE = 'code'
HEADER = 'application/x-www-form-urlencoded'

CLIENT_ID = '4648b6cee4344e04b4c2a46d2f83a1e6'
CLIENT_SECRET = 'b5512349cd434a04858487754e11d1e6'

PORT = '5600'
CALLBACK_URL = 'http://localhost'

REDIRECT_URI = '{}:{}/rest/api/v1/authorization/spotify-service/oauth2callback'.format(
    CALLBACK_URL, PORT
)
SCOPE = (
    'playlist-modify-public playlist-modify-private user-read-recently-played user-top-read '
    'user-modify-playback-state user-read-private'
)

auth_query_parameters = {
    'response_type': 'code',
    'redirect_uri': REDIRECT_URI,
    'scope': SCOPE,
}

URL_ARGS = 'client_id={}&response_type={}&redirect_uri={}&scope={}'.format(
    CLIENT_ID, RESPONSE_TYPE, REDIRECT_URI, SCOPE
)

AUTH_URL = '{}{}'.format(SPOTIFY_URL_AUTH, URL_ARGS)

client = MongoClient(host='mongo', port=27017)
db = client['aswe-pda']
db.authenticate('dev', 'dev')
authorization = db['authorization']


def getToken(code):

    body = {
        'grant_type': 'authorization_code',
        'code': str(code),
        'redirect_uri': REDIRECT_URI,
    }

    encoded = base64.b64encode(('{}:{}'.format(CLIENT_ID, CLIENT_SECRET)).encode())
    headers = {'Authorization': 'Basic {}'.format(encoded)}

    post_request = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=headers)

    respones_data = json.loads(post_request.text)
    access_token = respones_data['access_token']

    auth_header = {'Authorization': 'Bearer {}'.format(access_token)}

    return auth_header


def authorize(auth_token):
    code_payload = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': REDIRECT_URI,
    }

    return set_tokens(code_payload)


def refresh():
    document = authorization.find_one(
        {'service': 'spotify-service', 'type': 'refresh'}
    )

    code_payload = {
        'grant_type': 'refresh_token',
        'refresh_token': document_to_dict(document)
    }

    return set_tokens(code_payload)


def credentials_to_dict(credentials):
    """
    Convert credentials from google to dict.
    :param credentials: Credentials from google_auth_oauthlib.flow.
    :return: Credentials as dict.
    """
    return {'service': 'spotify-service', 'type': 'credentials', 'token': credentials}


def document_to_dict(document):
    """
    Convert document from mongodb to dict, so that it can be used with google.oauth2.credentials.
    :param document: Document from mongodb.
    :return: Document as dict.
    """
    return document['token']


def getAuthHeader():

    document = authorization.find_one(
        {'service': 'spotify-service', 'type': 'credentials'}
    )

    if document is None:
        return make_response({'error': 'You are not authorized.'}, 401), False
    else:
        auth_header = {'Authorization': 'Bearer {}'.format(document_to_dict(document))}
        return auth_header, True


def set_tokens(data):
    # python 3 or above
    if sys.version_info[0] >= 3:
        base64encoded = base64.b64encode(
            ('{}:{}'.format(CLIENT_ID, CLIENT_SECRET)).encode()
        )
        headers = {'Authorization': 'Basic {}'.format(base64encoded.decode())}
    else:
        base64encoded = base64.b64encode('{}:{}'.format(CLIENT_ID, CLIENT_SECRET))
        headers = {'Authorization': 'Basic {}'.format(base64encoded)}

    post_request = requests.post(SPOTIFY_URL_TOKEN, data=data, headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data['access_token']

    if access_token:
        authorization.replace_one(
            {'service': 'spotify-service', 'type': 'credentials'},
            credentials_to_dict(access_token),
            upsert=True
        )
        if 'refresh_token' in response_data:
            refresh_token = response_data['refresh_token']
            authorization.replace_one(
                {'service': 'spotify-service', 'type': 'refresh'},
                {'service': 'spotify-service', 'type': 'refresh', 'token': refresh_token},
                upsert=True
            )
        return True
    else:
        return False
