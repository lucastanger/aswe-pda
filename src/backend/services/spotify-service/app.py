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
        return make_response({'message': 'Authorization successful'}, 200)
    return make_response({'error': 'Authorization failed'}, 400)


def valid_token(resp):
    return resp is not None and not 'error' in resp


@app.route('/rest/api/v1/spotify/profile/<search_type>')
def profile_infos(search_type):

    auth_header, success = flask_spotify_auth.get_auth_header()

    if success:

        if search_type == 'info':
            data = profile.get_user_profile(auth_header)
        elif search_type == 'playlist':
            data = profile.get_user_playlists(auth_header)
        elif search_type == 'artists':
            data = profile.get_user_top(auth_header, 'artists')
        elif search_type == 'tracks':
            data = profile.get_user_top(auth_header, 'tracks')
        elif search_type == 'recent':
            data = profile.get_user_recently_played(auth_header)
        elif search_type == 'featured':
            data = profile.get_featured_playlists(auth_header)
        else:
            return 'Invalid Input', False

        if valid_token(data):
            return data
        else:
            flask_spotify_auth.refresh()
            profile_infos(search_type)
    else:
        return {'error': 'Could not get the authorization header'}


@app.route('/rest/api/v1/spotify/play')
def play():

    auth_header, success = flask_spotify_auth.get_auth_header()

    if success:
        if profile.start_music(auth_header):
            return {'message': 'Play'}
        return {'error': 'Something went wrong or music already playing'}
    else:
        return {'error': 'Could not authenticate'}


@app.route('/rest/api/v1/spotify/pause')
def pause():

    auth_header, success = flask_spotify_auth.get_auth_header()

    if success:
        if profile.pause_music(auth_header):
            return {'message': 'Pause'}
        return {'error': 'Something went wrong or music already paused'}
    else:
        return {'error': 'Could not authenticate'}


@app.route('/rest/api/v1/spotify/image')
def image():

    a_id = request.args['id']

    auth_header, success = flask_spotify_auth.get_auth_header()

    if success:
        img = profile.get_image_url(auth_header, a_id)

        if valid_token(img):
            return img
    else:
        return False


if __name__ == '__main__':
    app.run(port=5565, host='0.0.0.0')
