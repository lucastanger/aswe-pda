from flask_spotify_auth import getAuth, refreshAuth, getToken

# Add your client ID
CLIENT_ID = "4648b6cee4344e04b4c2a46d2f83a1e6"

# aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "b5512349cd434a04858487754e11d1e6"

# Port and callback url can be changed or ledt to localhost:5000
PORT = "5565"
CALLBACK_URL = "http://0.0.0.0"

# Add needed scope from spotify user
SCOPE = "streaming user-read-email user-read-private"

# token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}:{}/callback/".format(CALLBACK_URL, PORT), SCOPE)


def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback/".format(CALLBACK_URL, PORT))
    return TOKEN_DATA


def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()


def getAccessToken():
    return TOKEN_DATA