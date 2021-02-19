from flask import Flask, redirect, request, session, g, render_template
import flask_spotify_auth, profile
import json

app = Flask(__name__)
app.secret_key = 'some key for session'


@app.route("/")
def home():
    return "Spotify Service"


@app.route("/auth")
def auth():
    return redirect(flask_spotify_auth.AUTH_URL)


@app.route("/callback/")
def callback():

    auth_token = request.args['code']
    auth_header = flask_spotify_auth.authorize(auth_token)
    session['auth_header'] = auth_header

    return redirect("{}:{}/profile".format(flask_spotify_auth.CALLBACK_URL, flask_spotify_auth.PORT))


def valid_token(resp):
    return resp is not None and not 'error' in resp


@app.route("/profile")
def prof():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        profile_data = profile.getUserProfile(auth_header)

        playlist_data = profile.getUserPlaylists(auth_header)

        top_artist_data = profile.getUserTop(auth_header, 'artists')

        top_tracks_data = profile.getUserTop(auth_header, 'tracks')

        recently_played_data = profile.getUserRecentlyPlayed(auth_header)

        featured_playlist_data = profile.getFeaturedPlaylists(auth_header)

        if valid_token(profile_data):
            return json.dumps(playlist_data, indent=4)


@app.route("/play")
def play():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        play = profile.startMusic(auth_header)

        if valid_token(play):
            return "Play"


@app.route("/pause")
def pause():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        play = profile.pauseMusic(auth_header)

        if valid_token(play):
            return "Pause"


if __name__ == '__main__':
    app.run(port=5565, host="127.0.0.1")
