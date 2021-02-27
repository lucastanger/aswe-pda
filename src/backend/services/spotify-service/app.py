from flask import Flask, redirect, request, session, g, render_template
import flask_spotify_auth, profile
import json

app = Flask(__name__)
app.secret_key = 'some key for session'


@app.route('/')
def home():
    return 'Spotify Service'


@app.route('/auth')
def auth():
    return redirect(flask_spotify_auth.AUTH_URL)


@app.route('/callback/')
def callback():

    auth_token = request.args['code']
    auth_header = flask_spotify_auth.authorize(auth_token)
    session['auth_header'] = auth_header

    return redirect(
        '{}:{}/profile'.format(flask_spotify_auth.CALLBACK_URL, flask_spotify_auth.PORT)
    )


def valid_token(resp):
    return resp is not None and not 'error' in resp


@app.route('/profile')
def prof():
    if 'auth_header' in session:

        return 'Authentifizierung erfolgreich!'


@app.route('/profile/<search_type>')
def profileInfos(search_type):
    if 'auth_header' in session:
        auth_header = session['auth_header']

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
            return 'Invalid Input'

        if valid_token(data):
            return json.dumps(data, indent=4)


@app.route('/play')
def play():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        play = profile.startMusic(auth_header)

        if valid_token(play):
            return


@app.route('/pause')
def pause():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        play = profile.pauseMusic(auth_header)

        if valid_token(play):
            return


if __name__ == '__main__':
    app.run(port=5565, host='0.0.0.0')
