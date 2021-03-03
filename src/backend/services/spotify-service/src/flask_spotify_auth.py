import base64, json, sys, requests

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

PORT = '5565'
CALLBACK_URL = 'http://0.0.0.0'

REDIRECT_URI = '{}:{}/rest/api/v1/spotify/callback/'.format(CALLBACK_URL, PORT)
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

    # python 3 or above
    if sys.version_info[0] >= 3:
        base64encoded = base64.b64encode(
            ('{}:{}'.format(CLIENT_ID, CLIENT_SECRET)).encode()
        )
        headers = {'Authorization': 'Basic {}'.format(base64encoded.decode())}
    else:
        base64encoded = base64.b64encode('{}:{}'.format(CLIENT_ID, CLIENT_SECRET))
        headers = {'Authorization': 'Basic {}'.format(base64encoded)}

    post_request = requests.post(SPOTIFY_URL_TOKEN, data=code_payload, headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data['access_token']

    # use the access token to access Spotify API
    auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
    return auth_header
