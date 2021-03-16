from flask import Flask, request, session, make_response
from src import flask_spotify_auth, profile

app = Flask(__name__)
app.secret_key = 'some key for session'


@app.route('/rest/api/v1/spotify/auth')
def auth():
    return make_response({'authorization_url': flask_spotify_auth.AUTH_URL}, 200)


@app.route('/rest/api/v1/spotify/callback')
def callback():

    auth_token = request.args['code']
    result = flask_spotify_auth.authorize(auth_token)

    if result:
        return make_response({'message': 'Authorization successful'}, 201)
    return make_response({'error': 'Authorization failed'}, 401)


def valid_token(resp):
    return resp is not None and not 'error' in resp


@app.route('/rest/api/v1/spotify/profile/<search_type>')
def profileInfos(search_type):

    auth_header = flask_spotify_auth.getAuthHeader()

    if auth_header:

        if search_type == 'info':
            data = profile.getUserProfile(auth_header)
        elif search_type == 'playlist':
            data = profile.getUserPlaylists(auth_header)
        elif search_type == 'artists':
            data = profile.getUserTop(auth_header, 'artists')
        elif search_type == 'tracks':
            data = profile.getUserTop(auth_header, 'tracks')
        elif search_type == 'recent':
            data = profile.getUserRecentlyPlayed(auth_header)
        elif search_type == 'featured':
            data = profile.getFeaturedPlaylists(auth_header)
        else:
            return 'Invalid Input', False

        if valid_token(data):
            return data
    else:
        return (
            make_response({'error': 'Could not get the authorization header'}, 402),
            False,
        )


@app.route('/rest/api/v1/spotify/play')
def play():

    auth_header = flask_spotify_auth.getAuthHeader()

    if auth_header:
        play = profile.startMusic(auth_header)

        if valid_token(play):
            return make_response({'message': 'Play!'}, 200), True
    else:
        return (
            make_response({'error': 'Could not get the authorization header'}, 402),
            False,
        )


@app.route('/rest/api/v1/spotify/pause')
def pause():

    auth_header = flask_spotify_auth.getAuthHeader()

    if auth_header:
        pause = profile.pauseMusic(auth_header)

        if valid_token(pause):
            return make_response({'message': 'Pause!'}, 200), True
    else:
        return (
            make_response({'error': 'Could not get the authorization header'}, 402),
            False,
        )


if __name__ == '__main__':
    app.run(port=5565, host='0.0.0.0')
